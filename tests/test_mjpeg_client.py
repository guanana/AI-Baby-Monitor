import time
import sys
import os
import cv2

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from services.streaming.video_reader import MJPEGClient
except ImportError:
    # Handle case where imports might fail if not fully set up
    print("Could not import MJPEGClient. Ensure you are running from project root or have paths set.")
    sys.exit(1)

def test_mjpeg_client(url):
    print(f"Testing MJPEG Client with URL: {url}")
    
    client = None
    try:
        # Simple heuristic to choose client, similar to video_reader.py logic
        if url.lower().startswith(('http://', 'https://')):
             print("Using MJPEGClient (forcing for test)")
             client = MJPEGClient(url, verify_ssl=False)
        else:
             print("Using OpenCV VideoCapture")
             client = cv2.VideoCapture(url)
    except Exception as e:
        print(f"Failed to initialize client: {e}")
        return

    is_cv2 = isinstance(client, cv2.VideoCapture)

    if is_cv2:
        if not client.isOpened():
             print("Failed to open stream (OpenCV)")
             return
    elif not client.isOpened():
        print("Failed to open stream (MJPEGClient)")
        return

    print("Stream opened successfully. Reading frames...")
    
    start_time = time.time()
    frame_count = 0
    errors = 0
    
    try:
        while time.time() - start_time < 10: # Read for 10 seconds
            if is_cv2:
                ret, frame = client.read()
            else:
                ret, frame = client.read()
                
            if ret and frame is not None:
                frame_count += 1
                if frame_count % 10 == 0:
                     print(f"Read {frame_count} frames. Last frame shape: {frame.shape}")
            else:
                errors += 1
                if errors % 10 == 0:
                    print(f"Failed to read frame (Total errors: {errors})")
                time.sleep(0.01)
                
    except KeyboardInterrupt:
        pass
        
    print(f"Test finished. Total frames: {frame_count}, Total errors: {errors}")
    client.release()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 test_mjpeg_client.py <stream_url>")
        sys.exit(1)
        
    url = sys.argv[1]
    test_mjpeg_client(url)
