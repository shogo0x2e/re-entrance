import cv2
import os
from datetime import datetime
import time

class VideoRecorder:
    def __init__(self, cap=None, output_dir="./clips", fps=30):
        self.output_dir = output_dir
        self.fps = fps
        self.clip_duration = 60  # 1分間の録画
        self.frame_width = 1280
        self.frame_height = 720
        
        # 出力ディレクトリの作成
        os.makedirs(output_dir, exist_ok=True)
        
        self.cap = cap
        self.writer = None
        self.recording = False
        self.start_time = None
        self.frame_count = 0

    def start(self):
        """録画を開始します"""
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FPS, self.fps)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
        
        self.recording = True
        self.start_time = time.time()
        self._create_new_writer()
        
        while self.recording:
            ret, frame = self.cap.read()
            if not ret:
                break
                
            self.writer.write(frame)
            self.frame_count += 1
            
            # 1分経過したら新しいファイルを作成
            if time.time() - self.start_time >= self.clip_duration:
                self._create_new_writer()
                self.start_time = time.time()
                
            # 'q'キーで終了
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def stop(self):
        """録画を停止します"""
        self.recording = False
        if self.writer:
            self.writer.release()
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()

    def _create_new_writer(self):
        """新しい動画ファイルを作成します"""
        if self.writer:
            self.writer.release()
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"clip_{timestamp}.mp4")
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.writer = cv2.VideoWriter(
            output_path,
            fourcc,
            self.fps,
            (self.frame_width, self.frame_height)
        ) 