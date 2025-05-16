from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/api/v1/capturing-status")
def capturing_status():
    is_capturing = os.path.exists("/tmp/recording.lock")
    return {"capturing": is_capturing}

from datetime import datetime
from fastapi import HTTPException

@app.get("/api/video/{timestamp}")
async def get_video(timestamp: str):
    try:
        # ISO 8601形式のタイムスタンプをパース
        requested_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        
        # モック値を返す
        return {
            "video_url": f"http://example.com/videos/mock_{timestamp}.mp4",
            "start_time": (requested_time.isoformat() + "Z").replace("+00:00", "Z"),
            "duration": 40  # 前後20秒で合計40秒
        }
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid timestamp format. Please use ISO 8601 format (e.g. 2024-03-20T15:30:00Z)"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
