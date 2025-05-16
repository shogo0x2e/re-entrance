import cv2
import os
from datetime import datetime
    
# 1 つの動画ファイルの長さ
clip_length = 300

def main():
    # Web カメラの初期化
    cap = cv2.VideoCapture(0)
    
    # 保存先ディレクトリの作成
    if not os.path.exists("./clips"):
        os.makedirs("./clips")
    
    while True:
        # 現在時刻をファイル名に使用
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"./clips/video_{timestamp}.mp4"
        
        # 動画ファイルの設定
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(filename, fourcc, 20.0, (640,480))
        
        start_time = datetime.now()
        
        while (datetime.now() - start_time).seconds < clip_length:
            ret, frame = cap.read()
            if ret:
                out.write(frame)
                cv2.imshow('Recording...', frame)
                
                # q キーで終了
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cap.release()
                    out.release()
                    cv2.destroyAllWindows()
                    return
        
        out.release()

if __name__ == "__main__":
    main()
