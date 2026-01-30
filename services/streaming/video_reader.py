"""
Video streaming module for camera connectivity (RTSP & MJPEG)
"""
import cv2
import time
import threading
import numpy as np
import requests
from config.settings import config


class MJPEGClient:
    """
    Custom MJPEG stream reader using requests.
    Used primarily when specific SSL/TLS control is needed (e.g. self-signed certs).
    Mimics a subset of cv2.VideoCapture interface.
    """
    def __init__(self, url, verify_ssl=True):
        self.url = url
        self.verify_ssl = verify_ssl
        self.stream_response = None
        self.bytes_buffer = bytes()
        self._is_opened = False
        self._connect()
        
    def _connect(self):
        try:
            # Open the stream with requests
            # timeout is for the connection, not the stream duration
            print(f"[MJPEGClient] Connecting to {self.url} with verify_ssl={self.verify_ssl}...")
            self.stream_response = requests.get(
                self.url, 
                stream=True, 
                verify=self.verify_ssl, 
                timeout=10
            )
            print(f"[MJPEGClient] Connection status: {self.stream_response.status_code}")
            if self.stream_response.status_code == 200:
                self._is_opened = True
                # We need to iterate over the content
                self.iterator = self.stream_response.iter_content(chunk_size=1024)
            else:
                self._is_opened = False
        except Exception as e:
            print(f"[MJPEGClient] Connection error: {e}")
            self._is_opened = False

    def isOpened(self):
        return self._is_opened

    def read(self):
        """
        Reads the next frame from the MJPEG stream.
        Returns (ret, frame) similar to cv2.VideoCapture.
        """
        if not self._is_opened:
            return False, None

        # Basic MJPEG parsing logic: look for JPEG start/end markers
        # SOI (Start of Image): 0xFF 0xD8
        # EOI (End of Image):   0xFF 0xD9
        
        # We read chunks until we find a full frame
        # This is a blocking operation, but in a thread usually.
        # For simplicity and robustness, we buffer slightly efficiently.
        
        try:
            while True:
                # Search for start
                a = self.bytes_buffer.find(b'\xff\xd8')
                # Search for end
                b = self.bytes_buffer.find(b'\xff\xd9')
                
                if a != -1 and b != -1:
                    # We have a candidate frame
                    jpg = self.bytes_buffer[a:b+2]
                    # Shift buffer
                    self.bytes_buffer = self.bytes_buffer[b+2:]
                    
                    # Decode
                    frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    if frame is not None:
                        return True, frame
                    # If decode fails, we might have had garbage bytes looking like markers, continue
                    continue
                    
                # If we don't have a full frame, read more
                chunk = next(self.iterator)
                self.bytes_buffer += chunk
                
                # Safety break for buffer size to prevent OOM on broken streams
                if len(self.bytes_buffer) > 10 * 1024 * 1024: # 10MB limit
                     print(f"[MJPEGClient] Buffer size limit exceeded ({len(self.bytes_buffer)} bytes). Resetting buffer.")
                     self.bytes_buffer = bytes()
                     return False, None

        except StopIteration:
            self._is_opened = False
            return False, None
        except Exception as e:
            # print(f"[MJPEGClient] Read error: {e}")
            self._is_opened = False
            return False, None

    def grab(self):
        # Requests stream is linear, we can't easily skip without reading.
        # So grab() acts like read() but discards result? 
        # Or we just return True to simulate that a frame "could" be read.
        # For compatibility with the update loop which calls grab() then read(),
        # we can make grab() a no-op that returns True if opened.
        return self._is_opened

    def release(self):
        self._is_opened = False
        if self.stream_response:
            self.stream_response.close()
        
    def set(self, prop, val):
        pass  # ignore properties


class VideoReader:
    """Threaded Video stream reader with auto-reconnection (Supports RTSP & MJPEG)"""
    
    def __init__(self, url):
        """Initialize Video reader"""
        self.url = url
        self.cap = None
        self.connect()
        
        self.lock = threading.Lock()
        self.latest_frame = None
        self.stopped = False
        self.connection_lost = False
        
        # Start reading thread
        t = threading.Thread(target=self.update, daemon=True)
        t.start()
    
    def connect(self):
        """Try to connect to video stream (RTSP or MJPEG) with retries"""
        for attempt in range(config.MAX_RETRIES):
            try:
                print(f"[VIDEO] Attempting connection (attempt {attempt + 1}/{config.MAX_RETRIES})...")
                
                # Check if it's an HTTP/MJPEG stream
                if self.url.lower().startswith(('http://', 'https://')):
                     print(f"[VIDEO] Detected HTTP/MJPEG stream: {self.url}")
                     
                     if config.STREAM_SELF_SIGNED_CERT:
                         print("[VIDEO] Allowing self-signed certificates (using MJPEGClient)")
                         # Use custom client if we need to ignore SSL certs
                         self.cap = MJPEGClient(self.url, verify_ssl=False)
                     else:
                         # Use OpenCV default if standard
                         self.cap = cv2.VideoCapture(self.url)
                else:
                    # Assume RTSP or other ffmpeg supported stream
                    print(f"[VIDEO] Detected RTSP/Video stream: {self.url}")
                    self.cap = cv2.VideoCapture(self.url, cv2.CAP_FFMPEG)
                    # Set additional properties for better RTSP connection
                    self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                    self.cap.set(cv2.CAP_PROP_FPS, 25)
                
                if self.cap.isOpened():
                    # Test if we can actually read a frame
                    ret, frame = self.cap.read()
                    if ret and frame is not None:
                        print(f"[SUCCESS] Video connection successful!")
                        return
                    else:
                        self.cap.release()
                        print(f"[WARNING] Could not read from stream...")
                else:
                    print(f"[WARNING] Could not open stream with {self.url}")
                
                print(f"[ERROR] Connection attempt {attempt + 1} failed, retrying in {config.RETRY_DELAY} seconds...")
                time.sleep(config.RETRY_DELAY)
                
            except Exception as e:
                print(f"[ERROR] Connection error on attempt {attempt + 1}: {e}")
                time.sleep(config.RETRY_DELAY)
        
        raise RuntimeError(self._get_connection_error_message())
    
    def _get_connection_error_message(self):
        """Generate detailed error message for connection failure"""
        camera_ip = 'unknown'
        if '@' in self.url:
            camera_ip = self.url.split('@')[1].split('/')[0]
        elif '://' in self.url:
             camera_ip = self.url.split('://')[1].split('/')[0]

        return (f"[ERROR] Cannot open Video stream after {config.MAX_RETRIES} attempts. Please check:\n"
                f"1. Camera IP address: {camera_ip}\n"
                f"2. Username/password credentials\n"
                f"3. Network connectivity\n"
                f"4. Camera is powered on and accessible\n"
                f"5. URL is correct (RTSP or HTTP/MJPEG)")
    
    def update(self):
        """Background thread for reading frames"""
        consecutive_failures = 0
        
        while not self.stopped:
            if self.cap is None or not self.cap.isOpened():
                time.sleep(0.1)
                continue
                
            # Note: For OpenCV, grab() separates decoding from reading.
            # For our MJPEGClient, grab() is a no-op returning True.
            grabbed = self.cap.grab()
            if not grabbed:
                consecutive_failures += 1
                if consecutive_failures >= config.MAX_FAILURES:
                    print("[WARNING] Too many consecutive failures, attempting to reconnect...")
                    try:
                        self.cap.release()
                        self.connect()
                        consecutive_failures = 0
                        self.connection_lost = False
                    except Exception as e:
                        print(f"[ERROR] Reconnection failed: {e}")
                        self.connection_lost = True
                        time.sleep(5)  # Wait longer before next attempt
                else:
                    time.sleep(0.01)
                continue
            
            ret, frame = self.cap.read()
            if not ret or frame is None:
                consecutive_failures += 1
                time.sleep(0.01)
                continue
            
            # Reset failure counter on successful read
            consecutive_failures = 0
            self.connection_lost = False
            
            with self.lock:
                self.latest_frame = frame

    def read(self):
        """Get the latest frame"""
        with self.lock:
            return self.latest_frame.copy() if self.latest_frame is not None else None

    def stop(self):
        """Stop the reader and release resources"""
        self.stopped = True
        try:
            if self.cap:
                self.cap.release()
        except Exception:
            pass
