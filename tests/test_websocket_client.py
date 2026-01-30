import socketio
import time
import sys

# Create a Socket.IO client
sio = socketio.Client()

frame_count = 0
start_time = 0

@sio.event
def connect():
    print("Connected to WebSocket server")
    # Join the streaming room? The server code shows:
    # socket.emit('video_frame', ..., room='streaming_enabled')
    # Use standard mechanisms if the server expects authentication or specific events.
    # But usually joining a room is server-side logic based on auth. 
    # Let's see if we receive anything just by connecting.

@sio.event
def connect_error(data):
    print(f"Connection failed: {data}")

@sio.event
def disconnect():
    print("Disconnected from server")

@sio.on('video_frame')
def on_video_frame(data):
    global frame_count, start_time
    if frame_count == 0:
        start_time = time.time()
    frame_count += 1
    if frame_count % 10 == 0:
        elapsed = time.time() - start_time
        fps = frame_count / elapsed
        print(f"Received {frame_count} frames. Average FPS: {fps:.2f}")

def main():
    url = 'http://localhost:8847'
    print(f"Connecting to {url}...")
    try:
        sio.connect(url, wait_timeout=10)
        sio.wait()
    except Exception as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("Stopping...")
        sio.disconnect()

if __name__ == '__main__':
    main()
