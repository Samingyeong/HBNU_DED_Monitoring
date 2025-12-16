"""
FastAPI 백엔드 서버 - HBNU 모니터링 시스템
기존 PyQt 애플리케이션을 백엔드 API로 리팩토링
"""
import os
import sys
import asyncio
import json
import time
import logging
import io
import cv2
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
import uvicorn

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("HBNU_Backend")

# 프로젝트 루트 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.sensor_manager import SensorManager
from backend.data_storage import DataStorage
from backend.websocket_manager import WebSocketManager

# DED Log Reader 임포트
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Sensors"))
try:
    from ded_log_reader import DEDLogReader  # type: ignore
    DED_LOG_AVAILABLE = True
    logger.info("✅ DED Log Reader 모듈 임포트 성공")
except ImportError as e:
    logger.warning(f"⚠️ DED Log Reader 임포트 실패: {e}")
    DED_LOG_AVAILABLE = False


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
ded_log_reader: Optional['DEDLogReader'] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 생명주기 관리"""
    global sensor_manager, data_storage, websocket_manager, ded_log_reader
    
    logger.info("=" * 80)
    logger.info("🚀 HBNU DED 모니터링 백엔드 서버 시작 중...")
    logger.info("=" * 80)
    
    # CNC Subprocess 모드 설정 (환경 변수 또는 기본값)
    use_cnc_subprocess = os.getenv('USE_CNC_SUBPROCESS', 'false').lower() == 'true'
    cnc_python_path = os.getenv('CNC_PYTHON_EXECUTABLE', None)
    
    if use_cnc_subprocess:
        logger.info("📌 CNC Subprocess 모드 활성화 (32비트 호환성)")
        if cnc_python_path:
            logger.info(f"   Python 경로: {cnc_python_path}")
    
    # 센서 매니저 초기화
    logger.info("🔧 센서 매니저 초기화 시작...")
    sensor_manager = SensorManager(
        use_cnc_subprocess=use_cnc_subprocess,
        cnc_python_path=cnc_python_path
    )
    await sensor_manager.initialize()
    logger.info("✅ 센서 매니저 초기화 완료")
    
    # 연결 상태 로깅
    if sensor_manager.connection_status:
        logger.info("📊 센서 연결 상태:")
        for sensor_name, status in sensor_manager.connection_status.items():
            status_icon = "✅" if status else "❌"
            logger.info(f"   {status_icon} {sensor_name}: {'연결됨' if status else '연결 안됨'}")
    
    # 데이터 스토리지 초기화
    logger.info("💾 데이터 스토리지 초기화 중...")
    data_storage = DataStorage()
    logger.info("✅ 데이터 스토리지 초기화 완료")
    
    # WebSocket 매니저 초기화
    logger.info("🔌 WebSocket 매니저 초기화 중...")
    websocket_manager = WebSocketManager()
    logger.info("✅ WebSocket 매니저 초기화 완료")
    
    # DED Log Reader 초기화 (선택적 - Trace/Exception 파일이 없어도 센서는 작동)
    if DED_LOG_AVAILABLE:
        try:
            logger.info("📋 DED Log Reader 초기화 중...")
            ded_log_reader = DEDLogReader()
            logger.info("✅ DED Log Reader 초기화 완료")
            logger.info("   ℹ️  공정 시작 시 Trace/Exception 파일을 자동으로 읽습니다")
        except Exception as e:
            logger.warning(f"⚠️ DED Log Reader 초기화 실패: {e}")
            logger.info("   ℹ️  센서 데이터는 정상적으로 수집됩니다 (Trace/Exception 파일 없음)")
            ded_log_reader = None
    
    # 데이터 수집 태스크 시작
    logger.info("🔄 데이터 수집 태스크 시작 중...")
    data_collection_task = asyncio.create_task(collect_sensor_data())
    
    logger.info("=" * 80)
    logger.info("✅ 백엔드 서버 준비 완료 - API 서버 실행 중")
    logger.info(f"🌐 서버 주소: http://127.0.0.1:8000")
    logger.info(f"📚 API 문서: http://127.0.0.1:8000/docs")
    logger.info("=" * 80)
    
    yield
    
    # 정리 작업
    logger.info("=" * 80)
    logger.info("🛑 백엔드 서버 종료 중...")
    data_collection_task.cancel()
    if sensor_manager:
        logger.info("🔧 센서 매니저 정리 중...")
        await sensor_manager.cleanup()
    if ded_log_reader:
        logger.info("📋 DED Log Reader 정리 중...")
        ded_log_reader.stop()
    logger.info("✅ 백엔드 서버 종료 완료")
    logger.info("=" * 80)


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

# 요청 로깅 미들웨어
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # 요청 로깅 (더 상세하게)
    print(f"🌐 [{request.method}] {request.url.path}")  # print도 추가
    logger.info(f"🌐 [{request.method}] {request.url.path}")
    
    try:
        # 요청 처리
        response = await call_next(request)
        
        # 응답 시간 계산
        process_time = (time.time() - start_time) * 1000  # ms
        
        # 응답 로깅
        status_icon = "✅" if response.status_code < 400 else "❌"
        print(f"{status_icon} [{request.method}] {request.url.path} - {response.status_code} ({process_time:.2f}ms)")
        logger.info(f"{status_icon} [{request.method}] {request.url.path} - {response.status_code} ({process_time:.2f}ms)")
        
        return response
    except Exception as e:
        print(f"❌❌❌ 요청 처리 중 에러: {request.url.path} - {str(e)}")
        logger.error(f"❌ 요청 처리 중 에러: {request.url.path}", exc_info=True)
        raise


async def collect_sensor_data():
    """센서 데이터 수집 및 WebSocket 전송 (HBU_monitoring 방식 - 50Hz)"""
    collection_count = 0
    error_count = 0
    last_log_time = time.time()
    
    logger.info("🔄 센서 데이터 수집 루프 시작 (50Hz)")
    
    while True:
        try:
            if sensor_manager and data_storage:
                # 모든 센서 데이터 수집 (이미 Thread로 수집 중이므로 DB에서만 조회)
                sensor_data = await sensor_manager.collect_all_data()
                
                # 데이터 저장소에 저장
                data_storage.store_data(sensor_data)
                
                # WebSocket으로 실시간 전송
                if websocket_manager:
                    await websocket_manager.broadcast_data(sensor_data)
                
                collection_count += 1
                
                # 10초마다 수집 통계 로깅
                current_time = time.time()
                if current_time - last_log_time >= 10:
                    logger.info(f"📊 데이터 수집 통계: {collection_count}건 수집, 오류 {error_count}건 (최근 10초)")
                    collection_count = 0
                    error_count = 0
                    last_log_time = current_time
            
            # 20ms 간격으로 수집 (50Hz) - HBU_monitoring과 동일
            await asyncio.sleep(0.02)
            
        except Exception as e:
            error_count += 1
            logger.error(f"❌ 데이터 수집 오류: {e}")
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
    logger.debug("시스템 상태 조회 요청")
    
    if not sensor_manager:
        logger.error("센서 매니저가 초기화되지 않음")
        raise HTTPException(status_code=503, detail="센서 매니저가 초기화되지 않았습니다")
    
    status = await sensor_manager.get_connection_status()
    
    # 연결 상태 요약 로깅
    connected_count = sum(1 for s in status.values() if s)
    total_count = len(status)
    logger.debug(f"센서 연결 상태: {connected_count}/{total_count} 연결됨")
    
    return {
        "system_status": "running",
        "sensors": status,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/data/latest")
async def get_latest_data():
    """최신 센서 데이터 조회"""
    logger.debug("최신 센서 데이터 조회 요청")
    
    if not data_storage:
        logger.error("데이터 스토리지가 초기화되지 않음")
        raise HTTPException(status_code=503, detail="데이터 스토리지가 초기화되지 않았습니다")
    
    latest = data_storage.get_latest_data()
    
    if latest is None:
        logger.warning("⚠️ 최신 데이터가 없음 - 빈 객체 반환")
        return {
            "timestamp": datetime.now().isoformat(),
            "camera_data": None,
            "laser_data": None,
            "pyrometer_data": None,
            "cnc_data": None,
            "hik_camera_data": None
        }
    
    logger.debug(f"✅ 최신 데이터 반환: timestamp={latest.get('timestamp', 'N/A')}")
    return latest


@app.get("/api/data/history")
async def get_data_history(limit: int = 100):
    """히스토리 데이터 조회"""
    if not data_storage:
        raise HTTPException(status_code=503, detail="데이터 스토리지가 초기화되지 않았습니다")
    
    return data_storage.get_history_data(limit)


@app.post("/api/save/start")
async def start_saving(request: SaveRequest):
    """데이터 저장 시작 (수동 저장)"""
    global sensor_manager
    logger.info(f"💾 저장 시작 요청: folder={request.folder_name}")
    
    if not data_storage:
        logger.error("데이터 스토리지가 초기화되지 않음")
        raise HTTPException(status_code=503, detail="데이터 스토리지가 초기화되지 않았습니다")
    
    try:
        # 요청에 auto_save 플래그가 있으면 임시 저장으로 처리
        if hasattr(request, 'auto_save') and request.auto_save:
            await data_storage.start_temp_storage(request.folder_name)
            logger.info(f"✅ 임시 저장 시작됨: {request.folder_name}")
            return {
                "message": "임시 저장이 시작되었습니다",
                "save_path": f"temp_{request.folder_name}",
                "timestamp": datetime.now().isoformat(),
                "is_temp_storage": True
            }
        else:
            save_path = await data_storage.start_saving(request.folder_name)
            logger.info(f"✅ 데이터 저장 시작됨: {save_path}")
            
            # Basler 카메라 이미지 저장 시작 (공정 폴더 안에 basler_images 폴더)
            if sensor_manager and "camera" in sensor_manager.collectors:
                basler_save_dir = os.path.join(save_path, "basler_images")
                sensor_manager.collectors["camera"].set_save_dir(basler_save_dir)
                logger.info(f"📷 Basler 이미지 저장 시작: {basler_save_dir}")
            
            return {
                "message": "데이터 저장이 시작되었습니다",
                "save_path": save_path,
                "timestamp": datetime.now().isoformat(),
                "is_temp_storage": False
            }
    except Exception as e:
        logger.error(f"❌ 저장 시작 실패: {e}")
        raise HTTPException(status_code=500, detail=f"저장 시작 실패: {str(e)}")


@app.post("/api/save/stop")
async def stop_saving():
    """데이터 저장 중지"""
    global sensor_manager
    if not data_storage:
        raise HTTPException(status_code=503, detail="데이터 스토리지가 초기화되지 않았습니다")
    
    try:
        await data_storage.stop_saving()
        
        # Basler 카메라 이미지 저장 중지
        if sensor_manager and "camera" in sensor_manager.collectors:
            sensor_manager.collectors["camera"].stop_saving()
            logger.info("📷 Basler 이미지 저장 중지")
        
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
    print("🔍 temp-info 엔드포인트 호출됨")
    try:
        if not data_storage:
            print("❌ data_storage가 None입니다")
            raise HTTPException(status_code=503, detail="데이터 스토리지가 초기화되지 않았습니다")
        
        info = data_storage.get_temp_storage_info()
        print(f"✅ temp-info 반환: {info}")
        return info
    except Exception as e:
        print(f"❌ temp-info 에러: {str(e)}")
        raise


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
    """실시간 카메라 이미지 조회 (Basler, HikRobot) - 단일 프레임"""
    global sensor_manager
    
    if sensor_manager is None:
        raise HTTPException(status_code=503, detail="센서 매니저가 초기화되지 않았습니다")
    
    try:
        if image_type == "basler":
            # Basler 카메라에서 실시간 이미지 가져오기
            if sensor_manager.connection_status.get("camera") and "camera" in sensor_manager.databases:
                camera_data = sensor_manager.databases["camera"].retrieve_data()
                if camera_data and camera_data.get("image") is not None:
                    image = camera_data["image"]
                    # numpy array를 JPEG로 인코딩 (PNG보다 빠름)
                    _, buffer = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 80])
                    return StreamingResponse(
                        io.BytesIO(buffer.tobytes()),
                        media_type="image/jpeg",
                        headers={"Cache-Control": "no-cache, no-store, must-revalidate"}
                    )
            raise HTTPException(status_code=404, detail="Basler 카메라 이미지를 사용할 수 없습니다")
        
        elif image_type == "hik":
            # HikRobot 카메라에서 실시간 이미지 가져오기
            if (sensor_manager.connection_status.get("hik_camera_1") and 
                sensor_manager.connection_status.get("hik_camera_2")):
                hik_data = sensor_manager._get_combined_hik_image()
                if hik_data and hik_data.get("combined_image") is not None:
                    image = hik_data["combined_image"]
                    _, buffer = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 80])
                    return StreamingResponse(
                        io.BytesIO(buffer.tobytes()),
                        media_type="image/jpeg",
                        headers={"Cache-Control": "no-cache, no-store, must-revalidate"}
                    )
            raise HTTPException(status_code=404, detail="HikRobot 카메라 이미지를 사용할 수 없습니다")
        
        else:
            raise HTTPException(status_code=400, detail=f"알 수 없는 이미지 타입: {image_type}")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"이미지 조회 오류: {e}")
        raise HTTPException(status_code=500, detail=f"이미지 조회 실패: {str(e)}")


def generate_mjpeg_frames(image_type: str):
    """MJPEG 스트리밍용 프레임 제너레이터 (실시간 영상 스트리밍)"""
    global sensor_manager
    
    FRAME_INTERVAL = 0.033  # ~30fps (33ms)
    JPEG_QUALITY = 75  # 품질 (속도 vs 품질 균형)
    
    while True:
        try:
            frame = None
            
            if image_type == "basler":
                if (sensor_manager and 
                    sensor_manager.connection_status.get("camera") and 
                    "camera" in sensor_manager.databases):
                    camera_data = sensor_manager.databases["camera"].retrieve_data()
                    if camera_data and camera_data.get("image") is not None:
                        frame = camera_data["image"]
            
            elif image_type == "hik":
                if (sensor_manager and 
                    sensor_manager.connection_status.get("hik_camera_1") and 
                    sensor_manager.connection_status.get("hik_camera_2")):
                    hik_data = sensor_manager._get_combined_hik_image()
                    if hik_data and hik_data.get("combined_image") is not None:
                        frame = hik_data["combined_image"]
            
            if frame is not None:
                # JPEG로 인코딩 (PNG보다 훨씬 빠름)
                _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY])
                frame_bytes = buffer.tobytes()
                
                # MJPEG 프레임 형식으로 yield
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            else:
                # 프레임이 없으면 짧은 대기 후 재시도
                time.sleep(0.1)
                continue
            
            # 프레임 간격 유지 (30fps)
            time.sleep(FRAME_INTERVAL)
            
        except Exception as e:
            logger.warning(f"MJPEG 프레임 생성 오류: {e}")
            time.sleep(0.1)


@app.get("/api/stream/{image_type}")
async def stream_video(image_type: str):
    """MJPEG 실시간 비디오 스트리밍 (자연스러운 영상)"""
    global sensor_manager
    
    if sensor_manager is None:
        raise HTTPException(status_code=503, detail="센서 매니저가 초기화되지 않았습니다")
    
    if image_type not in ["basler", "hik"]:
        raise HTTPException(status_code=400, detail=f"알 수 없는 이미지 타입: {image_type}")
    
    # 카메라 연결 상태 확인
    if image_type == "basler" and not sensor_manager.connection_status.get("camera"):
        raise HTTPException(status_code=404, detail="Basler 카메라가 연결되지 않았습니다")
    
    if image_type == "hik" and not (sensor_manager.connection_status.get("hik_camera_1") and 
                                     sensor_manager.connection_status.get("hik_camera_2")):
        raise HTTPException(status_code=404, detail="HikRobot 카메라가 연결되지 않았습니다")
    
    logger.info(f"📹 MJPEG 스트리밍 시작: {image_type}")
    
    return StreamingResponse(
        generate_mjpeg_frames(image_type),
        media_type="multipart/x-mixed-replace; boundary=frame",
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
            "Connection": "keep-alive"
        }
    )


@app.get("/api/config/list")
async def get_config_list():
    """사용 가능한 config 파일 목록 조회"""
    logger.debug("📁 Config 파일 목록 조회 요청")
    
    try:
        config_dir = os.path.join(os.path.dirname(__file__), "..", "config")
        config_files = []
        
        if os.path.exists(config_dir):
            for file in os.listdir(config_dir):
                if file.endswith('.ini'):
                    config_files.append(file)
        
        logger.info(f"✅ Config 파일 {len(config_files)}개 발견: {', '.join(config_files)}")
        
        return {
            "success": True,
            "files": sorted(config_files),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"❌ Config 파일 목록 조회 실패: {e}")
        raise HTTPException(status_code=500, detail=f"설정 파일 목록 조회 실패: {str(e)}")


@app.get("/api/config/{file_name}")
async def get_config_file(file_name: str):
    """특정 config 파일 내용 조회"""
    logger.info(f"📄 Config 파일 조회 요청: {file_name}")
    
    try:
        # 보안: 파일명 검증 (../ 등 경로 조작 방지)
        if '..' in file_name or '/' in file_name or '\\' in file_name:
            logger.warning(f"⚠️ 잘못된 파일명 요청: {file_name}")
            raise HTTPException(status_code=400, detail="잘못된 파일명입니다")
        
        if not file_name.endswith('.ini'):
            logger.warning(f"⚠️ ini가 아닌 파일 요청: {file_name}")
            raise HTTPException(status_code=400, detail="ini 파일만 조회 가능합니다")
        
        config_path = os.path.join(os.path.dirname(__file__), "..", "config", file_name)
        
        if not os.path.exists(config_path):
            logger.warning(f"⚠️ 파일이 존재하지 않음: {config_path}")
            raise HTTPException(status_code=404, detail="설정 파일을 찾을 수 없습니다")
        
        # 파일 내용 읽기
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        logger.info(f"✅ Config 파일 읽기 성공: {file_name} ({len(content)} bytes)")
        
        return {
            "success": True,
            "file_name": file_name,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Config 파일 읽기 실패: {e}")
        raise HTTPException(status_code=500, detail=f"설정 파일 읽기 실패: {str(e)}")


@app.get("/api/ded-log/sessions")
async def get_ded_log_sessions():
    """DED 로그에서 과거 공정 세션 목록 조회"""
    if not ded_log_reader:
        raise HTTPException(status_code=503, detail="DED Log Reader를 사용할 수 없습니다")
    
    try:
        # 로그 파일 전체 분석하여 공정 세션 추출
        sessions = ded_log_reader.get_all_process_sessions()
        
        return {
            "success": True,
            "sessions": sessions,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DED 로그 세션 조회 실패: {str(e)}")


@app.get("/api/ded-log/current")
async def get_current_ded_log():
    """현재 진행 중인 공정 정보 조회"""
    if not ded_log_reader:
        raise HTTPException(status_code=503, detail="DED Log Reader를 사용할 수 없습니다")
    
    try:
        events = list(ded_log_reader.process_events)
        
        # 가장 최근 이벤트 확인
        is_running = False
        current_session = None
        
        if events:
            last_event = events[-1]
            if last_event['event'] in ['process_start', 'nc_start']:
                is_running = True
                current_session = {
                    'start_time': last_event['timestamp'],
                    'event_count': len(events)
                }
        
        return {
            "success": True,
            "is_running": is_running,
            "current_session": current_session,
            "recent_events": events[-10:] if len(events) > 0 else [],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"현재 DED 로그 조회 실패: {str(e)}")


## NC 기능 제거: 관련 모델 및 엔드포인트 삭제


# 파일 읽기 요청 모델
class FileReadRequest(BaseModel):
    """파일 읽기 요청 모델"""
    file_path: str


class FileExistsRequest(BaseModel):
    """파일 존재 확인 요청 모델"""
    file_path: str


@app.post("/api/file/read")
async def read_file(request: FileReadRequest):
    """로컬 파일 읽기 (Trace/Exception 파일 모니터링용)"""
    try:
        file_path = request.file_path
        
        # 보안: 허용된 경로만 읽기 (DED 로그 경로)
        allowed_paths = ['C:\\DED\\Log', 'D:\\DED\\Log', 'C:/DED/Log', 'D:/DED/Log']
        is_allowed = any(file_path.startswith(p) or file_path.replace('/', '\\').startswith(p) for p in allowed_paths)
        
        if not is_allowed:
            logger.warning(f"⚠️ 허용되지 않은 파일 경로 요청: {file_path}")
            return {"success": False, "error": "Access denied - path not allowed"}
        
        if not os.path.exists(file_path):
            return {"success": False, "error": "File not found"}
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        return {"success": True, "content": content}
    except Exception as e:
        logger.error(f"❌ 파일 읽기 실패: {e}")
        return {"success": False, "error": str(e)}


@app.post("/api/file/exists")
async def check_file_exists(request: FileExistsRequest):
    """파일 존재 여부 확인"""
    try:
        file_path = request.file_path
        
        # 보안: 허용된 경로만 확인
        allowed_paths = ['C:\\DED\\Log', 'D:\\DED\\Log', 'C:/DED/Log', 'D:/DED/Log']
        is_allowed = any(file_path.startswith(p) or file_path.replace('/', '\\').startswith(p) for p in allowed_paths)
        
        if not is_allowed:
            return {"exists": False}
        
        return {"exists": os.path.exists(file_path)}
    except Exception as e:
        logger.error(f"❌ 파일 존재 확인 실패: {e}")
        return {"exists": False}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket 연결 처리 (keepalive ping 포함)"""
    client_host = websocket.client.host if websocket.client else "unknown"
    print(f"🔌 WebSocket 연결 요청: {client_host}")
    logger.info(f"🔌 WebSocket 연결 요청: {client_host}")
    
    try:
        await websocket_manager.connect(websocket)
        print(f"✅ WebSocket 연결됨: {client_host} (총 {len(websocket_manager.active_connections)}개 연결)")
        logger.info(f"✅ WebSocket 연결됨: {client_host} (총 {len(websocket_manager.active_connections)}개 연결)")
        
        # 연결 유지 루프
        while True:
            try:
                # 30초 타임아웃으로 메시지 대기 (클라이언트로부터 pong 또는 메시지 수신)
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
                # 필요시 클라이언트 메시지 처리 로직 추가
                logger.debug(f"📨 WebSocket 메시지 수신: {client_host} - {data[:50]}")
            except asyncio.TimeoutError:
                # 타임아웃 시 ping 전송하여 연결 유지
                try:
                    await websocket.send_json({"type": "ping", "timestamp": datetime.now().isoformat()})
                    logger.debug(f"🏓 Keepalive ping 전송: {client_host}")
                except Exception as ping_error:
                    logger.warning(f"⚠️ Ping 전송 실패: {client_host} - {ping_error}")
                    raise  # 연결 끊김으로 처리
            except Exception as recv_error:
                logger.warning(f"⚠️ 메시지 수신 오류: {client_host} - {recv_error}")
                raise
                
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
        print(f"🔌 WebSocket 연결 해제: {client_host}")
        logger.info(f"🔌 WebSocket 연결 해제: {client_host}")
    except Exception as e:
        print(f"❌ WebSocket 에러: {str(e)}")
        logger.error(f"❌ WebSocket 에러: {client_host}", exc_info=True)
        websocket_manager.disconnect(websocket)
        logger.info(f"🔌 WebSocket 연결 해제: {client_host} (남은 연결: {len(websocket_manager.active_connections)}개)")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
