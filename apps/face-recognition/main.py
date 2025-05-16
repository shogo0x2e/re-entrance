import cv2

from face_recognition import FaceRecognizer

# カメラの初期化
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# 両方のクラスに同じカメラインスタンスを渡す
face_recognizer = FaceRecognizer(cap=cap)

if __name__ == "__main__":
    face_recognizer.run()