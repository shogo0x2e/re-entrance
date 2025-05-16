import cv2
import time
import mediapipe as mp
import numpy as np

# Mediapipe 初期化
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False,
                                   max_num_faces=1,
                                   refine_landmarks=True,
                                   min_detection_confidence=0.5,
                                   min_tracking_confidence=0.5)

# Webカメラ初期化
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Webカメラが開けません")
    exit()

# 特徴量を取得する間隔（秒）
interval = 0.5
last_time = 0

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 現在時刻取得
        current_time = time.time()

        # interval 経過していなければスキップ
        if current_time - last_time < interval:
            continue
        last_time = current_time

        # Mediapipe 用に画像を処理
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            face_landmarks = results.multi_face_landmarks[0]
            # 特徴点を np.array にまとめる（468点 * (x, y, z)）
            feature_vector = np.array([(lm.x, lm.y, lm.z) for lm in face_landmarks.landmark])
            feature_vector = feature_vector.flatten()
            
            # 過去3秒の特徴量を保持する配列を初期化（初回のみ）
            if not hasattr(face_mesh, 'feature_history'):
                face_mesh.feature_history = []
                face_mesh.time_history = []
            
            # 3秒以上前のデータを削除
            while (len(face_mesh.time_history) > 0 and 
                   current_time - face_mesh.time_history[0] > 3.0):
                face_mesh.feature_history.pop(0)
                face_mesh.time_history.pop(0)
            
            # コサイン類似度のチェック
            is_similar = False
            for past_feature in face_mesh.feature_history:
                cos_sim = np.dot(feature_vector, past_feature) / (
                    np.linalg.norm(feature_vector) * np.linalg.norm(past_feature))
                if cos_sim >= 0.9:
                    print("すでに検知しています")
                    is_similar = True
                    break
            
            if not is_similar:
                print("新しい顔を検知しました")
                face_mesh.feature_history.append(feature_vector)
                face_mesh.time_history.append(current_time)
        else:
            print("顔が検出されませんでした")

        # 表示（任意）
        cv2.imshow('Face Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    face_mesh.close()