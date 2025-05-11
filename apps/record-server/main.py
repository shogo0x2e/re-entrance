from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/check")
def check():
    is_capturing = os.path.exists("/tmp/recording.lock")
    return {"capturing": is_capturing}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
