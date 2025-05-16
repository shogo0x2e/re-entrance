import os
from datetime import datetime, timedelta
import glob
import logging

# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('re-entrance-videos-logs/cleanup.log'),
        logging.StreamHandler()
    ]
)

def cleanup_old_videos():
    logging.info("クリーンアップ処理を開始")
    # 録画保存先ディレクトリ
    videos_dir = os.path.expanduser("~/re-entrance-videos")
    
    # 2時間前の時刻を計算
    cutoff_time = datetime.utcnow() - timedelta(hours=2)
    logging.info(f"削除対象の基準時刻: {cutoff_time}")
    
    # ディレクトリ内のすべてのmp4ファイルを取得
    video_files = glob.glob(os.path.join(videos_dir, "*.mp4"))
    logging.info(f"対象ファイル数: {len(video_files)}")
    
    for video_file in video_files:
        try:
            # ファイル名からタイムスタンプを抽出
            filename = os.path.basename(video_file)
            timestamp_str = filename.replace(".mp4", "")
            file_time = datetime.strptime(timestamp_str, "%Y-%m-%dT%H-%M-%SZ")
            
            # 2時間以上前のファイルを削除
            if file_time < cutoff_time:
                os.remove(video_file)
                logging.info(f"削除: {video_file}")
            else:
                logging.debug(f"保持: {video_file} (作成時刻: {file_time})")
        except Exception as e:
            logging.error(f"エラー: {video_file} - {str(e)}")
    
    logging.info("クリーンアップ処理を終了")

if __name__ == "__main__":
    cleanup_old_videos()
