"""
FastAPI 백엔드 서버 - HBNU 모니터링 시스템
기존 PyQt 애플리케이션을 백엔드 API로 리팩토링
"""
import os
import sys
import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

# 프로젝트 루트 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.sensor_manager import SensorManager
from backend.data_storage import DataStorage
from backend.websocket_manager import WebSocketManager


class SensorData(BaseModel):
    """센서 데이터 모델"""
    timestamp: str
    camera_data: Optional[Dict] = None
    laser_data: Optional[Dict] = None
    pyrometer_data: Optional[Dict] = None
    cnc_data: Optional[Dict] = None
    hik_camera_data: Optional[Dict] = None


class SaveRequest(BaseModel):
    """데이터 저장 요청 모델"""
    folder_name: str
    auto_save: Optional[bool] = False
    dest_path: Optional[str] = None


# 전역 변수
sensor_manager: Optional[SensorManager] = None
data_storage: Optional[DataStorage] = None
websocket_manager: Optional[WebSocketManager] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 생명주기 관리"""
    global sensor_manager, data_storage, websocket_manager
    
    print("🚀 백엔드 서버 시작 중...")
    
    # 센서 매니저 초기화
    sensor_manager = SensorManager()
    await sensor_manager.initialize()
    
    # 데이터 스토리지 초기화
    data_storage = DataStorage()
    
    # WebSocket 매니저 초기화
    websocket_manager = WebSocketManager()
    
    # 데이터 수집 태스크 시작
    data_collection_task = asyncio.create_task(collect_sensor_data())
    
    print("✅ 백엔드 서버 준비 완료")
    
    yield
    
    # 정리 작업
    print("🛑 백엔드 서버 종료 중...")
    data_collection_task.cancel()
    if sensor_manager:
        await sensor_manager.cleanup()
    print("✅ 백엔드 서버 종료 완료")


# FastAPI 앱 생성
app = FastAPI(
    title="HBNU Monitoring Backend",
    description="DED 모니터링 시스템 백엔드 API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 환경에서만 사용, 프로덕션에서는 특정 도메인 지정
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def collect_sensor_data():
    """센서 데이터 수집 및 WebSocket 전송"""
    while True:
        try:
            if sensor_manager and data_storage:
                # 모든 센서 데이터 수집
                sensor_data = await sensor_manager.collect_all_data()
                
                # 데이터 저장소에 저장
                data_storage.store_data(sensor_data)
                
                # WebSocket으로 실시간 전송
                if websocket_manager:
                    await websocket_manager.broadcast_data(sensor_data)
            
            # 100ms 간격으로 수집 (10Hz)
            await asyncio.sleep(0.1)
            
        except Exception as e:
            print(f"❌ 데이터 수집 오류: {e}")
            await asyncio.sleep(1)


# API 엔드포인트들
@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "HBNU Monitoring Backend API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/api/status")
async def get_status():
    """시스템 상태 조회"""
    if not sensor_manager:
        raise HTTPException(status_code=503, detail="센서 매니저가 초기화되지 않았습니다")
    
    status = await sensor_manager.get_connection_status()
    return {
        "system_status": "running",
        "sensors": status,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/data/latest")
async def get_latest_data():
    """최신 센서 데이터 조회"""
    if not data_storage:
        raise HTTPException(status_code=503, detail="데이터 스토리지가 초기화되지 않았습니다")
    
    return data_storage.get_latest_data()


@app.get("/api/data/history")
async def get_data_history(limit: int = 100):
    """히스토리 데이터 조회"""
    if not data_storage:
        raise HTTPException(status_code=503, detail="데이터 스토리지가 초기화되지 않았습니다")
    
    return data_storage.get_history_data(limit)


@app.post("/api/save/start")
async def start_saving(request: SaveRequest):
    """데이터 저장 시작 (수동 저장)"""
    if not data_storage:
        raise HTTPException(status_code=503, detail="데이터 스토리지가 초기화되지 않았습니다")
    
    try:
        # 요청에 auto_save 플래그가 있으면 임시 저장으로 처리
        if hasattr(request, 'auto_save') and request.auto_save:
            await data_storage.start_temp_storage(request.folder_name)
            return {
                "message": "임시 저장이 시작되었습니다",
                "save_path": f"temp_{request.folder_name}",
                "timestamp": datetime.now().isoformat(),
                "is_temp_storage": True
            }
        else:
            save_path = await data_storage.start_saving(request.folder_name)
            return {
                "message": "데이터 저장이 시작되었습니다",
                "save_path": save_path,
                "timestamp": datetime.now().isoformat(),
                "is_temp_storage": False
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"저장 시작 실패: {str(e)}")


@app.post("/api/save/stop")
async def stop_saving():
    """데이터 저장 중지"""
    if not data_storage:
        raise HTTPException(status_code=503, detail="데이터 스토리지가 초기화되지 않았습니다")
    
    try:
        await data_storage.stop_saving()
        return {
            "message": "데이터 저장이 중지되었습니다",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"저장 중지 실패: {str(e)}")


@app.post("/api/save/temp-stop")
async def stop_temp_saving():
    """임시 저장 중지 (자동저장 종료 시)"""
    if not data_storage:
        raise HTTPException(status_code=503, detail="데이터 스토리지가 초기화되지 않았습니다")
    
    try:
        await data_storage.stop_temp_storage()
        return {
            "message": "임시 저장이 중지되었습니다",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"임시 저장 중지 실패: {str(e)}")


@app.post("/api/save/temp-to-permanent")
async def save_temp_to_permanent(request: SaveRequest):
    """임시 저장된 데이터를 영구 저장으로 이동"""
    if not data_storage:
        raise HTTPException(status_code=503, detail="데이터 스토리지가 초기화되지 않았습니다")
    
    try:
        if getattr(request, 'dest_path', None):
            save_path = await data_storage.save_temp_storage_to_path(request.dest_path)  # 사용자 지정 경로
        else:
            save_path = await data_storage.save_temp_storage_to_permanent(request.folder_name)
        return {
            "message": "임시 데이터가 영구 저장되었습니다",
            "save_path": save_path,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"임시 데이터 영구 저장 실패: {str(e)}")


@app.get("/api/save/temp-info")
async def get_temp_storage_info():
    """임시 저장 정보 조회"""
    if not data_storage:
        raise HTTPException(status_code=503, detail="데이터 스토리지가 초기화되지 않았습니다")
    
    return data_storage.get_temp_storage_info()


@app.get("/api/save/status")
async def get_save_status():
    """저장 상태 조회"""
    if not data_storage:
        raise HTTPException(status_code=503, detail="데이터 스토리지가 초기화되지 않았습니다")
    
    return {
        "is_saving": data_storage.is_saving,
        "save_path": data_storage.current_save_path,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/images/{image_type}")
async def get_image(image_type: str):
    """이미지 파일 조회 (카메라, HikRobot 등)"""
    # 이미지 파일 경로 생성
    image_path = f"backend/images/{image_type}_latest.png"
    
    if os.path.exists(image_path):
        return FileResponse(image_path)
    else:
        raise HTTPException(status_code=404, detail="이미지를 찾을 수 없습니다")


## NC 기능 제거: 관련 모델 및 엔드포인트 삭제


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket 연결 처리"""
    await websocket_manager.connect(websocket)
    try:
        while True:
            # 클라이언트로부터 메시지 수신 대기
            data = await websocket.receive_text()
            # 필요시 클라이언트 메시지 처리 로직 추가
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
