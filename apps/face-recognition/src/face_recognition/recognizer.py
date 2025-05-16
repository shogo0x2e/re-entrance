import cv2
import time
import mediapipe as mp
import numpy as np

class FaceRecognizer:
    def __init__(self, cap=None, video_recorder=None):
        # 特徴量を取得する間隔（秒）
        self.interval = 0.5
        self.last_time = 0
        self.last_cache_clear_time = 0  # キャッシュをクリアした最後の時刻

        # 顔の最大量
        self.max_num_faces = 10

        # キャッシュをクリアする間隔（秒）
        self.cache_clear_interval = 5

        # 同一人物と判定する Cosine Similarity の閾値
        self.cosine_similarity_threshold = 0.90

        # 特徴量のキャッシュを保持するリスト
        self.feature_cache = []

        # Mediapipe 初期化
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=self.max_num_faces,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        self.cap = cap
        self.video_recorder = video_recorder

    def initialize_camera(self):
        """カメラの初期化を行う"""
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                raise RuntimeError("Webカメラが開けません")
        return self.cap

    def should_process_frame(self, current_time):
        """フレームを処理すべきかどうかを判定"""
        return current_time - self.last_time >= self.interval

    def should_clear_cache(self, current_time):
        """キャッシュをクリアすべきかどうかを判定"""
        return current_time - self.last_cache_clear_time >= self.cache_clear_interval

    def clear_cache(self):
        """キャッシュをクリア"""
        self.feature_cache.clear()
        print("キャッシュをクリアしました")

    def process_face_landmarks(self, face_landmarks):
        """顔のランドマークから特徴ベクトルを生成"""
        feature_vector = np.array([(lm.x, lm.y, lm.z) for lm in face_landmarks.landmark])
        return feature_vector.flatten()

    def is_unique_face(self, feature_vector):
        """特徴ベクトルが既存のキャッシュ内でユニークかどうかを判定"""
        for cached_feature in self.feature_cache[:-1]:
            cosine_similarity = np.dot(feature_vector, cached_feature) / (
                np.linalg.norm(feature_vector) * np.linalg.norm(cached_feature)
            )
            if cosine_similarity > self.cosine_similarity_threshold:
                return False
        return True

    def process_frame(self, frame):
        """1フレームの処理"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for face_idx, face_landmarks in enumerate(results.multi_face_landmarks):
                feature_vector = self.process_face_landmarks(face_landmarks)
                self.feature_cache.append(feature_vector)
                is_unique = self.is_unique_face(feature_vector)
                
                print(f"顔 {face_idx + 1}/{len(results.multi_face_landmarks)} の特徴量:", 
                      feature_vector[:10], "... ユニーク:", is_unique)
        else:
            print("顔が検出されませんでした")

        return frame

    def run(self):
        """メインループ"""
        try:
            while True:
                # VideoRecorderからフレームを取得
                if self.video_recorder:
                    frame = self.video_recorder.get_current_frame()
                    if frame is None:
                        continue
                else:
                    ret, frame = self.cap.read()
                    if not ret:
                        break

                current_time = time.time()

                if self.should_clear_cache(current_time):
                    self.clear_cache()
                    self.last_cache_clear_time = current_time

                if not self.should_process_frame(current_time):
                    continue
                
                self.last_time = current_time
                
                processed_frame = self.process_frame(frame)

                # 表示（任意）
                cv2.imshow('Face Detection', processed_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        finally:
            if not self.video_recorder and self.cap:
                self.cap.release()
            cv2.destroyAllWindows()
            self.face_mesh.close() 