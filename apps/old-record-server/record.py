import subprocess
import os
import time
from datetime import datetime

LOCK_FILE = "/tmp/recording.lock"
VIDEO_DIR = "/home/pi/videos"

def wait_for_camera():
    while not os.path.exists("/dev/video0"):
        print("Waiting for camera...")
        time.sleep(10)

def main():
    os.makedirs(VIDEO_DIR, exist_ok=True)
    
    # カメラの接続を待機
    wait_for_camera()
    
    # lockファイルを作成
    with open(LOCK_FILE, "w") as f:
        f.write(datetime.now().isoformat())

    try:
        subprocess.run([
            "ffmpeg",
            "-f", "v4l2",
            "-input_format", "mjpeg",
            "-video_size", "1280x720",
            "-i", "/dev/video0",
            "-c:v", "copy",
            "-f", "segment",
            "-segment_time", "300",
            "-reset_timestamps", "1",
            "-strftime", "1",
            f"{VIDEO_DIR}/%Y%m%d_%H%M%S.mkv"
        ])
    except Exception as e:
        print("ffmpeg error:", e)
    finally:
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)

if __name__ == "__main__":
    main() 