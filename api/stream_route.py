"""
MJPEG Streaming Routes
"""
from flask import Blueprint, Response
from flask_login import login_required
from services.streaming.streaming_service import get_streaming_service
import cv2
import time

stream_bp = Blueprint('stream', __name__)

def gen_frames():
    """Frame generator for MJPEG stream"""
    streaming_service = get_streaming_service()
    if not streaming_service:
        return
    
    while True:
        if streaming_service.ai_streamer:
            frame = streaming_service.ai_streamer.get_latest_frame()
            if frame is not None:
                # Use slightly lower quality for MJPEG to save bandwidth
                ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
                if ret:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        
        # Limit to ~20 FPS for the web preview
        time.sleep(0.05)

@stream_bp.route('/video_feed')
@login_required
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
