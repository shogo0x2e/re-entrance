import subprocess
import os
from datetime import datetime
import time

def record_video():
    # 録画保存先ディレクトリの作成
    videos_dir = os.path.expanduser("~/re-entrance-videos")
    os.makedirs(videos_dir, exist_ok=True)

    while True:
        # 現在時刻をISO 8601形式で取得
        start_time = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%SZ")
        output_path = os.path.join(videos_dir, f"{start_time}.mp4")

        # ffmpegコマンドの構築
        ffmpeg_cmd = [
            "/usr/bin/ffmpeg",
            "-f", "v4l2",              # Video4Linux2フォーマット
            "-i", "/dev/video0",       # カメラデバイス
            "-t", "300",               # 録画時間（5分 = 300秒）
            "-c:v", "libx264",         # H.264エンコーダー
            "-preset", "ultrafast",    # エンコード速度優先
            "-pix_fmt", "yuv420p",     # ピクセルフォーマット
            output_path
        ]

        try:
            # 録画実行
            subprocess.run(ffmpeg_cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"録画エラー: {e}")
            time.sleep(10)  # エラー時は10秒待機
            continue

if __name__ == "__main__":
    record_video()
