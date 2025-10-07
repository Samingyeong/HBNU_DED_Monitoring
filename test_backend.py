#!/usr/bin/env python3
"""
테스트 백엔드 서버 - 실제 센서 데이터 시뮬레이션
실제 장비 센서와 연결된 것처럼 데이터를 생성하고 전송
"""
import asyncio
import json
import time
import random
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

# --- Pydantic 모델 정의 ---
class CNCData(BaseModel):
    curpos_x: float
    curpos_y: float
    curpos_z: float
    curpos_a: float
    curpos_c: float
    macpos_x: float
    macpos_y: float
    macpos_z: float
    macpos_a: float
    macpos_c: float
    feed_rate: float
    feed_override: float
    rapid_override: float
    feeder1_rpm: int
    feeder1_remaining: int
    feeder1_status: bool
    feeder2_rpm: int
    feeder2_remaining: int
    feeder2_status: bool
    feeder3_rpm: int
    feeder3_remaining: int
    feeder3_status: bool
    coaxial_gas: float
    feeding_gas: float
    shield_gas: float

class LaserData(BaseModel):
    outpower: float
    setpower: float

class PyrometerData(BaseModel):
    mpt: float
    one_ct: float
    two_ct: float

class CameraData(BaseModel):
    image: str # Base64 인코딩된 이미지 데이터 또는 URL
    melt_pool_area: float

class HikCameraData(BaseModel):
    combined_image: str # Base64 인코딩된 이미지 데이터 또는 URL

class SensorData(BaseModel):
    timestamp: str
    cnc_data: CNCData
    laser_data: LaserData
    pyrometer_data: PyrometerData
    camera_data: CameraData
    hik_camera_data: HikCameraData

class SaveRequest(BaseModel):
    folder_name: str

# --- 전역 변수 및 상태 관리 ---
class AppState:
    def __init__(self):
        self.latest_data: Optional[SensorData] = None
        self.history_data: List[SensorData] = []
        self.max_history = 500
        self.is_saving = False
        self.current_save_path: Optional[str] = None
        self.websocket_connections: List[WebSocket] = []
        self.emergency_stop = False

    def store_data(self, data: SensorData):
        self.latest_data = data
        self.history_data.append(data)
        if len(self.history_data) > self.max_history:
            self.history_data.pop(0)

    async def broadcast_data(self, data: SensorData):
        message = {"type": "sensor_data", "data": data.dict()}
        for connection in self.websocket_connections:
            try:
                await connection.send_json(message)
            except RuntimeError:
                # 연결이 끊어진 경우 처리
                self.websocket_connections.remove(connection)

    async def connect_websocket(self, websocket: WebSocket):
        await websocket.accept()
        self.websocket_connections.append(websocket)

    def disconnect_websocket(self, websocket: WebSocket):
        if websocket in self.websocket_connections:
            self.websocket_connections.remove(websocket)

app_state = AppState()

# --- FastAPI 애플리케이션 생명주기 ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 테스트 백엔드 서버 시작 중...")
    
    # 데이터 수집 태스크 시작
    data_collection_task = asyncio.create_task(collect_simulated_data())
    
    print("✅ 테스트 백엔드 서버 준비 완료 (시뮬레이션 모드)")
    
    yield
    
    # 정리 작업
    print("🛑 테스트 백엔드 서버 종료 중...")
    data_collection_task.cancel()
    print("✅ 테스트 백엔드 서버 종료 완료")

app = FastAPI(
    title="HBNU Monitoring Test Backend",
    description="DED 모니터링 시스템 테스트 백엔드 API (시뮬레이션)",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 시뮬레이션 데이터 생성 로직 ---
async def collect_simulated_data():
    """시뮬레이션 센서 데이터 수집 및 WebSocket 전송"""
    cycle = 0
    while True:
        try:
            if app_state.emergency_stop:
                # 비상 정지 시 데이터 업데이트 중지
                await asyncio.sleep(1)
                continue

            now = datetime.now()
            timestamp_str = now.isoformat()
            
            # CNC 데이터 시뮬레이션 (부드러운 변화)
            cnc_base_x = 15.0 + 2 * math.sin(cycle * 0.05)
            cnc_base_y = 64.0 + 1 * math.cos(cycle * 0.03)
            cnc_base_z = -0.05 + 0.01 * math.sin(cycle * 0.07)
            
            cnc_data = CNCData(
                curpos_x=round(cnc_base_x + random.uniform(-0.1, 0.1), 2),
                curpos_y=round(cnc_base_y + random.uniform(-0.1, 0.1), 2),
                curpos_z=round(cnc_base_z + random.uniform(-0.01, 0.01), 2),
                curpos_a=round(random.uniform(-0.5, 0.5), 2),
                curpos_c=round(random.uniform(-0.5, 0.5), 2),
                macpos_x=round(cnc_base_x + 10 + random.uniform(-0.1, 0.1), 2),
                macpos_y=round(cnc_base_y + 10 + random.uniform(-0.1, 0.1), 2),
                macpos_z=round(cnc_base_z + 5 + random.uniform(-0.01, 0.01), 2),
                macpos_a=round(random.uniform(-1.0, 1.0), 2),
                macpos_c=round(random.uniform(-1.0, 1.0), 2),
                feed_rate=round(random.uniform(1000, 5000), 0),
                feed_override=round(random.uniform(90, 110), 0),
                rapid_override=round(random.uniform(90, 110), 0),
                feeder1_rpm=random.randint(100, 1500),
                feeder1_remaining=random.randint(0, 100),
                feeder1_status=random.choice([True, False]),
                feeder2_rpm=random.randint(100, 1500),
                feeder2_remaining=random.randint(0, 100),
                feeder2_status=random.choice([True, False]),
                feeder3_rpm=random.randint(100, 1500),
                feeder3_remaining=random.randint(0, 100),
                feeder3_status=random.choice([True, False]),
                coaxial_gas=round(random.uniform(5, 20), 1),
                feeding_gas=round(random.uniform(5, 20), 1),
                shield_gas=round(random.uniform(5, 20), 1),
            )

            # Laser 데이터 시뮬레이션
            laser_data = LaserData(
                outpower=round(random.uniform(500, 1000), 1),
                setpower=1000.0
            )

            # Pyrometer 데이터 시뮬레이션 (용융지 온도)
            pyrometer_data = PyrometerData(
                mpt=round(random.uniform(1500, 2000), 1),
                one_ct=round(random.uniform(1400, 1900), 1),
                two_ct=round(random.uniform(1600, 2100), 1),
            )

            # Camera 데이터 시뮬레이션 (이미지는 더미, 용융지 면적)
            camera_data = CameraData(
                image="dummy_base64_image_data_camera",
                melt_pool_area=round(random.uniform(0.5, 2.5), 2)
            )

            # HikCamera 데이터 시뮬레이션 (이미지는 더미)
            hik_camera_data = HikCameraData(
                combined_image="dummy_base64_image_data_hikcamera"
            )
            
            sensor_data = SensorData(
                timestamp=timestamp_str,
                cnc_data=cnc_data,
                laser_data=laser_data,
                pyrometer_data=pyrometer_data,
                camera_data=camera_data,
                hik_camera_data=hik_camera_data
            )
            
            app_state.store_data(sensor_data)
            await app_state.broadcast_data(sensor_data)
            
            cycle += 1
            await asyncio.sleep(0.1) # 100ms 간격으로 데이터 생성 (10Hz)
            
        except asyncio.CancelledError:
            print("데이터 수집 태스크 종료")
            break
        except Exception as e:
            print(f"❌ 시뮬레이션 데이터 수집 오류: {e}")
            await asyncio.sleep(1)

# --- API 엔드포인트들 ---
@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "HBNU Monitoring Test Backend API",
        "version": "1.0.0",
        "status": "running",
        "mode": "simulation"
    }

@app.get("/api/status")
async def get_status():
    """시스템 상태 조회 (시뮬레이션)"""
    return {
        "system_status": "running",
        "sensors": {
            "camera": True,
            "laser": True,
            "pyrometer": True,
            "cnc": True,
            "hik_camera_1": True,
            "hik_camera_2": True,
        },
        "timestamp": datetime.now().isoformat(),
        "emergency_stop": app_state.emergency_stop
    }

@app.get("/api/data/latest")
async def get_latest_data():
    """최신 센서 데이터 조회"""
    if not app_state.latest_data:
        raise HTTPException(status_code=404, detail="데이터를 찾을 수 없습니다")
    return app_state.latest_data

@app.get("/api/data/history")
async def get_data_history(limit: int = 100):
    """히스토리 데이터 조회"""
    return app_state.history_data[-limit:]

@app.post("/api/save/start")
async def start_saving(request: SaveRequest):
    """데이터 저장 시작 (시뮬레이션)"""
    app_state.is_saving = True
    app_state.current_save_path = f"/simulated/data/{request.folder_name}"
    return {
        "message": "시뮬레이션 데이터 저장이 시작되었습니다",
        "save_path": app_state.current_save_path,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/save/stop")
async def stop_saving():
    """데이터 저장 중지 (시뮬레이션)"""
    app_state.is_saving = False
    app_state.current_save_path = None
    return {
        "message": "시뮬레이션 데이터 저장이 중지되었습니다",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/save/status")
async def get_save_status():
    """저장 상태 조회 (시뮬레이션)"""
    return {
        "is_saving": app_state.is_saving,
        "save_path": app_state.current_save_path,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/emergency/toggle")
async def toggle_emergency(emergency: bool):
    """비상 정지 상태 토글"""
    app_state.emergency_stop = emergency
    return {"message": f"Emergency stop set to {emergency}", "emergency": emergency}

@app.get("/api/images/{image_type}")
async def get_image(image_type: str):
    """이미지 파일 조회 (더미 이미지)"""
    # 실제 이미지 파일 대신 더미 이미지 반환
    dummy_image_path = "backend/images/dummy_image.png" # 실제 경로에 더미 이미지 필요
    if not os.path.exists(dummy_image_path):
        # 간단한 투명 PNG 생성 (필요시)
        from PIL import Image
        img = Image.new('RGBA', (640, 480), (255, 0, 0, 0))
        img.save(dummy_image_path)
    return FileResponse(dummy_image_path, media_type="image/png")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket 연결 처리"""
    await app_state.connect_websocket(websocket)
    try:
        while True:
            # 클라이언트로부터 메시지 수신 대기 (keep-alive 또는 제어 메시지)
            await websocket.receive_text() 
    except WebSocketDisconnect:
        app_state.disconnect_websocket(websocket)
    except Exception as e:
        print(f"WebSocket 오류: {e}")
        app_state.disconnect_websocket(websocket)

if __name__ == "__main__":
    uvicorn.run(
        "test_backend:app",
        host="127.0.0.1",
        port=8001, # 테스트 백엔드는 8001 포트 사용
        reload=True,
        log_level="info"
    )
