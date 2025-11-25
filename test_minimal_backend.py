"""
최소한의 FastAPI 백엔드 테스트
센서 초기화 없이 API만 테스트
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MinimalBackend")

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Minimal Backend Running"}

@app.get("/api/status")
async def get_status():
    logger.info("✅ /api/status 호출됨")
    return {
        "camera": False,
        "laser": False,
        "pyrometer": False,
        "cnc": False,
        "hik_camera": False
    }

@app.get("/api/data/latest")
async def get_latest():
    logger.info("✅ /api/data/latest 호출됨")
    return {
        "timestamp": "2025-11-25T08:45:00",
        "camera_data": None,
        "laser_data": None,
        "pyrometer_data": None,
        "cnc_data": None,
        "hik_camera_data": None
    }

@app.get("/api/save/status")
async def get_save_status():
    logger.info("✅ /api/save/status 호출됨")
    return {
        "is_saving": False,
        "folder_name": None,
        "start_time": None
    }

if __name__ == "__main__":
    logger.info("🚀 최소 백엔드 서버 시작...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")


