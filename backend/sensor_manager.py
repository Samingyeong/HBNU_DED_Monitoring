"""
센서 매니저 - 모든 센서의 통신과 데이터 수집을 관리
기존 센서 통신 모듈들을 비동기적으로 관리
"""
import asyncio
import sys
import os
from typing import Dict, Optional, Any
from datetime import datetime

# 프로젝트 루트 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 센서 모듈 임포트 (선택적)
try:
    from Sensors.camera_comm import CameraCommunication, CameraDB, CameraCollector
    CAMERA_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ 카메라 모듈 임포트 실패: {e}")
    CAMERA_AVAILABLE = False

try:
    from Sensors.laser_comm import LaserCommunication, LaserDB, IPG_Collector
    LASER_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ 레이저 모듈 임포트 실패: {e}")
    LASER_AVAILABLE = False

try:
    from Sensors.pyrometer_comm import PyrometerCommunication, PyrometerDB, PyrometerCollector
    PYROMETER_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Pyrometer 모듈 임포트 실패: {e}")
    PYROMETER_AVAILABLE = False

try:
    from Sensors.cnc_comm import CNCCommunication, CNC_DB, CNC_Collector
    CNC_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ CNC 모듈 임포트 실패: {e}")
    CNC_AVAILABLE = False

# CNC Subprocess Manager (32비트 호환성)
try:
    from backend.cnc_subprocess_manager import CNCSubprocessManager
    CNC_SUBPROCESS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ CNC Subprocess Manager 임포트 실패: {e}")
    CNC_SUBPROCESS_AVAILABLE = False

try:
    from Sensors.vision2 import HikCameraThread
    HIKCAMERA_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ HikRobot 카메라 모듈 임포트 실패: {e}")
    HIKCAMERA_AVAILABLE = False


class SensorManager:
    """센서 통신 및 데이터 수집을 관리하는 클래스"""
    
    def __init__(self, use_cnc_subprocess: bool = False, cnc_python_path: str = None):
        """
        Args:
            use_cnc_subprocess: True면 CNC를 subprocess로 실행 (32비트 호환성)
            cnc_python_path: 32비트 Python 실행 파일 경로
        """
        self.sensors = {}
        self.collectors = {}
        self.databases = {}
        self.connection_status = {}
        self.hik_cam_threads = {}
        self.use_cnc_subprocess = use_cnc_subprocess
        self.cnc_subprocess_manager = None
        
        # 센서별 연결 상태
        self.connection_status = {
            "camera": False,
            "laser": False,
            "pyrometer": False,
            "cnc": False,
            "hik_camera_1": False,
            "hik_camera_2": False
        }
    
    async def initialize(self):
        """모든 센서 초기화"""
        print("🔧 센서 매니저 초기화 중...")
        
        # 각 센서를 비동기적으로 초기화
        await asyncio.gather(
            self._initialize_camera(),
            self._initialize_laser(),
            self._initialize_pyrometer(),
            self._initialize_cnc(),
            self._initialize_hik_cameras(),
            return_exceptions=True
        )
        
        # 테스트 모드 설정 (센서가 없는 경우)
        self.test_mode = not any(self.connection_status.values())
        if self.test_mode:
            print("🧪 테스트 모드 활성화 (센서 없음)")
        
        print("✅ 센서 매니저 초기화 완료")
    
    async def _initialize_camera(self):
        """Basler 카메라 초기화"""
        if not CAMERA_AVAILABLE:
            print("⚠️ 카메라 모듈이 사용 불가능합니다")
            self.connection_status["camera"] = False
            return
            
        try:
            print("📷 Basler 카메라 연결 시도 중...")
            
            # 비동기 실행을 위해 스레드 풀 사용
            loop = asyncio.get_event_loop()
            
            # 센서 초기화
            self.sensors["camera"] = await loop.run_in_executor(
                None, CameraCommunication
            )
            self.databases["camera"] = CameraDB()
            self.collectors["camera"] = CameraCollector(
                self.sensors["camera"], 
                self.databases["camera"]
            )
            
            # 컬렉터 시작
            self.collectors["camera"].start()
            self.connection_status["camera"] = True
            
            print("✅ Basler 카메라 연결 성공")
            
        except Exception as e:
            print(f"❌ Basler 카메라 연결 실패: {e}")
            self.connection_status["camera"] = False
    
    async def _initialize_laser(self):
        """IPG 레이저 초기화"""
        if not LASER_AVAILABLE:
            print("⚠️ 레이저 모듈이 사용 불가능합니다")
            self.connection_status["laser"] = False
            return
            
        try:
            print("🔴 IPG 레이저 연결 시도 중...")
            
            loop = asyncio.get_event_loop()
            
            self.sensors["laser"] = await loop.run_in_executor(
                None, LaserCommunication
            )
            self.databases["laser"] = LaserDB()
            self.collectors["laser"] = IPG_Collector(
                self.sensors["laser"],
                self.databases["laser"]
            )
            
            self.collectors["laser"].start()
            self.connection_status["laser"] = True
            
            print("✅ IPG 레이저 연결 성공")
            
        except Exception as e:
            print(f"❌ IPG 레이저 연결 실패: {e}")
            self.connection_status["laser"] = False
    
    async def _initialize_pyrometer(self):
        """Pyrometer 초기화"""
        if not PYROMETER_AVAILABLE:
            print("⚠️ Pyrometer 모듈이 사용 불가능합니다")
            self.connection_status["pyrometer"] = False
            return
            
        try:
            print("🌡️ Pyrometer 연결 시도 중...")
            
            loop = asyncio.get_event_loop()
            
            self.sensors["pyrometer"] = await loop.run_in_executor(
                None, PyrometerCommunication
            )
            self.databases["pyrometer"] = PyrometerDB()
            self.collectors["pyrometer"] = PyrometerCollector(
                self.sensors["pyrometer"],
                self.databases["pyrometer"]
            )
            
            self.collectors["pyrometer"].start()
            self.connection_status["pyrometer"] = True
            
            print("✅ Pyrometer 연결 성공")
            
        except Exception as e:
            print(f"❌ Pyrometer 연결 실패: {e}")
            self.connection_status["pyrometer"] = False
    
    async def _initialize_cnc(self):
        """HXApi CNC 초기화 (subprocess 옵션 지원)"""
        # Subprocess 모드 사용
        if self.use_cnc_subprocess:
            if not CNC_SUBPROCESS_AVAILABLE:
                print("⚠️ CNC Subprocess Manager가 사용 불가능합니다")
                self.connection_status["cnc"] = False
                return
            
            try:
                print("🔧 HXApi CNC 연결 시도 중... (Subprocess 모드)")
                
                # 설정 파일 경로 설정
                config_path = os.path.join(
                    os.path.dirname(os.path.dirname(__file__)),
                    "config", "HXApi.ini"
                )
                
                # 환경 변수에서 Python 경로 읽기 (선택적)
                cnc_python_path = os.getenv('CNC_PYTHON_EXECUTABLE', None)
                
                # Subprocess Manager 생성 및 시작
                self.cnc_subprocess_manager = CNCSubprocessManager(
                    python_executable=cnc_python_path,
                    config_path=config_path
                )
                self.cnc_subprocess_manager.start()
                
                # DB는 subprocess에서 직접 사용하지 않으므로 None
                self.databases["cnc"] = None
                self.connection_status["cnc"] = True
                
                print("✅ HXApi CNC 연결 성공 (Subprocess 모드)")
                
            except Exception as e:
                print(f"❌ HXApi CNC 연결 실패 (Subprocess): {e}")
                self.connection_status["cnc"] = False
                return
        
        # 직접 DLL 로드 모드 (기존 방식)
        else:
            if not CNC_AVAILABLE:
                print("⚠️ CNC 모듈이 사용 불가능합니다")
                self.connection_status["cnc"] = False
                return
                
            try:
                print("🔧 HXApi CNC 연결 시도 중... (직접 DLL 로드)")
                
                loop = asyncio.get_event_loop()
                
                # 설정 파일 경로 설정
                config_path = os.path.join(
                    os.path.dirname(os.path.dirname(__file__)),
                    "config", "HXApi.ini"
                )
                
                self.sensors["cnc"] = await loop.run_in_executor(
                    None, CNCCommunication, config_path
                )
                self.databases["cnc"] = CNC_DB()
                self.collectors["cnc"] = CNC_Collector(
                    self.sensors["cnc"],
                    self.databases["cnc"]
                )
                
                self.collectors["cnc"].start()
                self.connection_status["cnc"] = True
                
                print("✅ HXApi CNC 연결 성공 (직접 DLL 로드)")
                
            except Exception as e:
                print(f"❌ HXApi CNC 연결 실패: {e}")
                self.connection_status["cnc"] = False
    
    async def _initialize_hik_cameras(self):
        """HikRobot 카메라 2대 초기화"""
        if not HIKCAMERA_AVAILABLE:
            print("⚠️ HikRobot 카메라 모듈이 사용 불가능합니다")
            self.connection_status["hik_camera_1"] = False
            self.connection_status["hik_camera_2"] = False
            return
            
        try:
            print("📹 HikRobot 카메라 연결 시도 중...")
            
            # HikRobot 카메라 1
            def push_hik_frame_1(frame):
                self.latest_frame1 = frame
            
            def push_hik_frame_2(frame):
                self.latest_frame2 = frame
            
            self.hik_cam_threads["hik_camera_1"] = HikCameraThread(
                "02J81094725", 
                on_new_frame=push_hik_frame_1, 
                parent=self
            )
            self.hik_cam_threads["hik_camera_1"].start()
            self.connection_status["hik_camera_1"] = True
            
            # HikRobot 카메라 2
            self.hik_cam_threads["hik_camera_2"] = HikCameraThread(
                "02J75405689", 
                on_new_frame=push_hik_frame_2, 
                parent=self
            )
            self.hik_cam_threads["hik_camera_2"].start()
            self.connection_status["hik_camera_2"] = True
            
            # 프레임 저장 변수 초기화
            self.latest_frame1 = None
            self.latest_frame2 = None
            
            print("✅ HikRobot 카메라 연결 성공")
            
        except Exception as e:
            print(f"❌ HikRobot 카메라 연결 실패: {e}")
            self.connection_status["hik_camera_1"] = False
            self.connection_status["hik_camera_2"] = False
    
    async def collect_all_data(self) -> Dict[str, Any]:
        """
        모든 센서에서 데이터 수집 (HBU_monitoring 방식)
        각 센서는 이미 Thread로 독립적으로 수집 중이므로 DB에서만 조회
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        
        sensor_data = {
            "timestamp": timestamp,
            "camera_data": None,
            "laser_data": None,
            "pyrometer_data": None,
            "cnc_data": None,
            "hik_camera_data": None
        }
        
        # 테스트 모드에서 더미 데이터 생성
        if getattr(self, 'test_mode', False):
            import random
            import time
            current_time = time.time()
            
            sensor_data.update({
                "camera_data": {
                    "melt_pool_area": round(10 + 5 * random.random(), 2),
                    "image_available": True
                },
                "laser_data": {
                    "outpower": round(400 + 100 * random.random(), 1),
                    "setpower": 500.0
                },
                "pyrometer_data": {
                    "mpt": round(1600 + 200 * random.random(), 1),
                    "1ct": round(1580 + 200 * random.random(), 1),
                    "2ct": round(1620 + 200 * random.random(), 1)
                },
                "cnc_data": {
                    "curpos_x": round(10 + 5 * random.random(), 2),
                    "curpos_y": round(20 + 5 * random.random(), 2),
                    "curpos_z": round(5 + 2 * random.random(), 2),
                    "curpos_a": 0.0,
                    "curpos_c": 0.0,
                    "feed_rate": 1000,
                    "feed_override": 100.0,
                    "rapid_override": 100.0
                },
                "hik_camera_data": {
                    "hik_image_available": True
                }
            })
            return sensor_data
        
        # 각 센서 DB에서 최신 데이터 조회 (비동기 실행으로 블로킹 방지)
        loop = asyncio.get_event_loop()
        
        # 카메라 데이터
        if self.connection_status["camera"] and "camera" in self.databases:
            try:
                camera_data = await loop.run_in_executor(
                    None, self.databases["camera"].retrieve_data
                )
                if camera_data:
                    sensor_data["camera_data"] = camera_data
            except Exception as e:
                print(f"⚠️ 카메라 데이터 수집 오류: {e}")
        
        # 레이저 데이터
        if self.connection_status["laser"] and "laser" in self.databases:
            try:
                laser_data = await loop.run_in_executor(
                    None, self.databases["laser"].retrieve_data
                )
                if laser_data:
                    sensor_data["laser_data"] = laser_data
            except Exception as e:
                print(f"⚠️ 레이저 데이터 수집 오류: {e}")
        
        # Pyrometer 데이터
        if self.connection_status["pyrometer"] and "pyrometer" in self.databases:
            try:
                pyrometer_data = await loop.run_in_executor(
                    None, self.databases["pyrometer"].retrieve_data
                )
                if pyrometer_data:
                    sensor_data["pyrometer_data"] = pyrometer_data
            except Exception as e:
                print(f"⚠️ Pyrometer 데이터 수집 오류: {e}")
        
        # CNC 데이터
        if self.connection_status["cnc"]:
            try:
                if self.use_cnc_subprocess and self.cnc_subprocess_manager:
                    # Subprocess 모드: subprocess manager에서 데이터 가져오기
                    cnc_data = self.cnc_subprocess_manager.get_latest_data()
                    if cnc_data:
                        sensor_data["cnc_data"] = cnc_data
                elif "cnc" in self.databases and self.databases["cnc"]:
                    # 직접 DLL 모드: DB에서 데이터 가져오기
                    cnc_data = await loop.run_in_executor(
                        None, self.databases["cnc"].retrieve_data
                    )
                    if cnc_data:
                        sensor_data["cnc_data"] = cnc_data
            except Exception as e:
                print(f"⚠️ CNC 데이터 수집 오류: {e}")
        
        # HikRobot 카메라 데이터
        if (self.connection_status["hik_camera_1"] and 
            self.connection_status["hik_camera_2"]):
            try:
                hik_data = self._get_combined_hik_image()
                if hik_data:
                    sensor_data["hik_camera_data"] = hik_data
            except Exception as e:
                print(f"⚠️ HikRobot 데이터 수집 오류: {e}")
        
        return sensor_data
    
    def _get_combined_hik_image(self) -> Optional[Dict]:
        """HikRobot 2대 이미지를 합쳐서 반환"""
        if hasattr(self, 'latest_frame1') and hasattr(self, 'latest_frame2'):
            if self.latest_frame1 is not None and self.latest_frame2 is not None:
                import cv2
                try:
                    h1, w1 = self.latest_frame1.shape[:2]
                    h2, w2 = self.latest_frame2.shape[:2]
                    h = max(h1, h2)
                    
                    f1 = cv2.resize(self.latest_frame1, (w1, h))
                    f2 = cv2.resize(self.latest_frame2, (w2, h))
                    combined = cv2.hconcat([f1, f2])
                    
                    return {
                        "combined_image": combined,
                        "frame1_shape": self.latest_frame1.shape,
                        "frame2_shape": self.latest_frame2.shape,
                        "combined_shape": combined.shape
                    }
                except Exception as e:
                    print(f"⚠️ HikRobot 이미지 합치기 오류: {e}")
        return None
    
    async def get_connection_status(self) -> Dict[str, bool]:
        """연결 상태 조회"""
        return self.connection_status.copy()
    
    async def cleanup(self):
        """리소스 정리"""
        print("🧹 센서 매니저 정리 중...")
        
        # CNC Subprocess 정지
        if self.cnc_subprocess_manager:
            try:
                self.cnc_subprocess_manager.stop()
                print("✅ CNC subprocess 정지 완료")
            except Exception as e:
                print(f"⚠️ CNC subprocess 정지 오류: {e}")
        
        # 모든 컬렉터 정지
        for name, collector in self.collectors.items():
            try:
                collector.stop()
                collector.join(timeout=5)
                print(f"✅ {name} 컬렉터 정지 완료")
            except Exception as e:
                print(f"⚠️ {name} 컬렉터 정지 오류: {e}")
        
        # HikRobot 카메라 정지
        for name, thread in self.hik_cam_threads.items():
            try:
                thread.stop()
                thread.join(timeout=5)
                print(f"✅ {name} 스레드 정지 완료")
            except Exception as e:
                print(f"⚠️ {name} 스레드 정지 오류: {e}")
        
        # 센서 연결 종료
        for name, sensor in self.sensors.items():
            try:
                if hasattr(sensor, 'close'):
                    sensor.close()
                print(f"✅ {name} 센서 연결 종료 완료")
            except Exception as e:
                print(f"⚠️ {name} 센서 연결 종료 오류: {e}")
        
        print("✅ 센서 매니저 정리 완료")
