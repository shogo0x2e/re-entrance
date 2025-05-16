import cv2

from face_recognition import FaceRecognizer
from src.video_recorder import VideoRecorder

# カメラの初期化
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# 両方のクラスに同じカメラインスタンスを渡す
video_recorder = VideoRecorder(cap=cap)
face_recognizer = FaceRecognizer(cap=cap)

if __name__ == "__main__":
    try:
        # 録画開始
        video_recorder.start()
        # 顔認識開始 
        face_recognizer.run()
    except KeyboardInterrupt:
        print("録画を停止します...")
    finally:
        video_recorder.stop()