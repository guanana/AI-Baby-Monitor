"""
Camera Service Layer - Handles camera operations and abstracts camera controller logic
"""
import logging
import threading
import time
from typing import Dict, List, Optional, Any
from services.controller.tapo_camera import TapoCameraController
from config.settings import config


class CameraService:
    """Service layer for camera operations with proper separation of concerns."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._controller = None
        self._is_enabled = config.CAMERA_ENABLED
        self._host = config.CAMERA_HOST
        self._username = config.CAMERA_USERNAME
        self._password = config.CAMERA_PASSWORD
        
        # Caching and locking
        self._cache_lock = threading.Lock()
        self._last_status = None
        self._last_presets = None
        self._last_update_time = 0
        self._cache_duration = 30  # Cache for 30 seconds
        
        # Thread for background initialization
        self._init_thread = None
        self._is_initializing = False

    def _get_controller(self):
        """Get or create camera controller instance."""
        if not self._is_enabled:
            return None
            
        if self._controller is None:
            if self._is_initializing:
                return None
                
            try:
                # Ensure we have valid credentials
                if not self._host or not self._username or not self._password:
                    self.logger.error("Camera credentials not properly configured")
                    return None
                
                # Start initialization in background to not block the web thread
                self._is_initializing = True
                self._init_thread = threading.Thread(target=self._background_init, daemon=True)
                self._init_thread.start()
                return None
            except Exception as e:
                self.logger.error(f"Failed to start camera controller initialization: {e}")
                self._is_initializing = False
                return None
                
        return self._controller
        
    def _background_init(self):
        """Perform camera initialization in background."""
        try:
            self.logger.info(f"Starting background camera initialization for {self._host}...")
            controller = TapoCameraController(
                host=self._host,
                username=self._username,
                password=self._password,
                debug=False
            )
            self._controller = controller
            self.logger.info("Camera controller initialized successfully via background thread")
        except Exception as e:
            self.logger.error(f"Background camera initialization failed: {e}")
        finally:
            self._is_initializing = False

    def is_available(self) -> bool:
        """Check if camera service is available."""
        return self._is_enabled and self._controller is not None
    
    def get_status(self) -> Dict[str, Any]:
        """Get camera status with caching."""
        if not self._is_enabled:
            return {
                'available': False,
                'reason': 'disabled',
                'device_model': 'Camera Disabled',
                'privacy_mode': False,
                'connection_status': 'disabled'
            }
        
        # Check cache
        with self._cache_lock:
            current_time = time.time()
            if self._last_status and (current_time - self._last_update_time < self._cache_duration):
                return self._last_status

        controller = self._get_controller()
        if not controller:
            return {
                'available': False,
                'reason': 'initializing' if self._is_initializing else 'offline',
                'device_model': 'Initializing...' if self._is_initializing else 'Offline',
                'privacy_mode': False,
                'connection_status': 'initializing' if self._is_initializing else 'offline'
            }
        
        try:
            # Add timeout protection specifically for these calls if the underlying lib allows it,
            # otherwise trust threading to keep the app responsive.
            basic_info = controller.get_basic_info()
            privacy_mode = controller.get_privacy_mode()
            
            # Ensure privacy_mode is always a boolean
            if privacy_mode is None:
                privacy_mode = False
            elif not isinstance(privacy_mode, bool):
                privacy_mode = bool(privacy_mode)
            
            # Extract device model
            device_model = 'Unknown'
            if isinstance(basic_info, dict):
                try:
                    device_model = basic_info.get('device_info', {}).get('basic_info', {}).get('device_alias', 'Unknown')
                except AttributeError:
                    device_model = 'Tapo Camera'
            
            status = {
                'available': True,
                'reason': 'connected',
                'device_model': device_model,
                'privacy_mode': privacy_mode,
                'connection_status': 'online',
            }
            
            with self._cache_lock:
                self._last_status = status
                self._last_update_time = time.time()
                
            return status
        except Exception as e:
            self.logger.error(f"Error getting camera status: {e}")
            return {
                'available': False,
                'reason': 'error',
                'device_model': 'Error',
                'privacy_mode': False,
                'connection_status': 'error',
                'error': str(e)
            }
    
    def get_presets(self) -> List[Dict[str, Any]]:
        """Get camera presets with caching."""
        # Use default presets if disabled or not yet connected
        default_presets = [
            {'id': 1, 'name': 'Home Position'},
            {'id': 2, 'name': 'Sleep Area'},
            {'id': 3, 'name': 'Play Area'}
        ]
        
        if not self._is_enabled:
            return default_presets
            
        # Check cache
        with self._cache_lock:
            current_time = time.time()
            if self._last_presets and (current_time - self._last_update_time < self._cache_duration):
                return self._last_presets

        controller = self._get_controller()
        if not controller:
            return default_presets
        
        try:
            presets = controller.get_presets()
            formatted_presets = []
            
            if isinstance(presets, list) and len(presets) > 0:
                for preset_data in presets:
                    if isinstance(preset_data, dict):
                        for preset_id, preset_name in preset_data.items():
                            try:
                                formatted_presets.append({
                                    'id': int(preset_id),
                                    'name': preset_name
                                })
                            except (ValueError, TypeError):
                                formatted_presets.append({
                                    'id': preset_id,
                                    'name': preset_name
                                })
                    else:
                        formatted_presets.append({
                            'id': len(formatted_presets) + 1,
                            'name': f'Preset {len(formatted_presets) + 1}'
                        })
            
            if not formatted_presets:
                formatted_presets = default_presets
            
            with self._cache_lock:
                self._last_presets = formatted_presets
                # Note: last_update_time is shared with status
            
            return formatted_presets
            
        except Exception as e:
            self.logger.error(f"Error getting presets: {e}")
            return default_presets


class CameraControlService:
    """Service layer for camera control operations."""
    
    def __init__(self, camera_service: CameraService):
        self.camera_service = camera_service
        self.logger = logging.getLogger(__name__)
    
    def set_preset(self, preset_id: int) -> Dict[str, Any]:
        """Set camera to specific preset position."""
        if not self.camera_service.is_available():
            return {'success': False, 'error': 'Camera is not ready yet'}
            
        controller = self.camera_service._controller
        
        try:
            success = controller.set_preset(preset_id)
            if success:
                return {
                    'success': True,
                    'message': f'Camera moved to preset {preset_id}',
                    'preset_id': preset_id
                }
            else:
                return {'success': False, 'error': 'Failed to set camera preset'}
        except Exception as e:
            self.logger.error(f"Error setting camera preset: {e}")
            return {'success': False, 'error': str(e)}
    
    def set_privacy_mode(self, enabled: bool) -> Dict[str, Any]:
        """Toggle camera privacy mode."""
        if not self.camera_service.is_available():
            return {'success': False, 'error': 'Camera is not ready yet'}
            
        controller = self.camera_service._controller
        
        try:
            success = controller.set_privacy_mode(enabled)
            if success:
                # Update cache immediately on manual change
                with self.camera_service._cache_lock:
                    if self.camera_service._last_status:
                        self.camera_service._last_status['privacy_mode'] = enabled
                        
                return {
                    'success': True,
                    'privacy_mode': enabled,
                    'message': f'Privacy mode {"enabled" if enabled else "disabled"}'
                }
            else:
                return {'success': False, 'error': 'Failed to toggle privacy mode'}
        except Exception as e:
            self.logger.error(f"Error toggling privacy mode: {e}")
            return {'success': False, 'error': str(e)}


# Global service instances
camera_service = CameraService()
camera_control_service = CameraControlService(camera_service)
