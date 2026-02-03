"""
센서 매니저 - 모든 센서의 통신과 데이터 수집을 관리
기존 센서 통신 모듈들을 비동기적으로 관리

GoF 패턴 적용:
- Factory Pattern: SensorFactory를 통한 센서 객체 생성
- Strategy Pattern: 센서별 통신 전략 (Socket, Serial, DLL)
- Template Method: BaseSensor 공통 로직
"""
import asyncio
import sys
import os
import logging
from typing import Dict, Optional, Any
from datetime import datetime

# 로거 설정
logger = logging.getLogger("HBNU_Backend")

# 프로젝트 루트 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ============================================
# GoF 패턴 기반 새 센서 모듈 (Factory Pattern)
# ============================================
try:
    from sensors import SensorFactory, ISensor
    from sensors.camera import CameraSensor
    from sensors.laser import LaserSensor
    from sensors.pyrometer import PyrometerSensor
    from sensors.cnc import CnCSensor
    NEW_SENSORS_AVAILABLE = True
    logger.info("✅ GoF 패턴 기반 센서 모듈 로드 완료")
except ImportError as e:
    NEW_SENSORS_AVAILABLE = False
    logger.warning(f"⚠️ 새 센서 모듈 임포트 실패 (레거시 모드 사용): {e}")

# ============================================
# 레거시 센서 모듈 (기존 호환성 유지)
# ============================================
try:
    from Sensors.camera_comm import CameraCommunication, CameraDB, CameraCollector
    CAMERA_AVAILABLE = True
except ImportError as e:
    logger.warning(f"카메라 모듈 임포트 실패: {e}")
    CAMERA_AVAILABLE = False

try:
    from Sensors.laser_comm import LaserCommunication, LaserDB, IPG_Collector
    LASER_AVAILABLE = True
except ImportError as e:
    logger.warning(f"레이저 모듈 임포트 실패: {e}")
    LASER_AVAILABLE = False

try:
    from Sensors.pyrometer_comm import PyrometerCommunication, PyrometerDB, PyrometerCollector
    PYROMETER_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Pyrometer 모듈 임포트 실패: {e}")
    PYROMETER_AVAILABLE = False

try:
    from Sensors.cnc_comm import CNCCommunication, CNC_DB, CNC_Collector
    CNC_AVAILABLE = True
except ImportError as e:
    logger.warning(f"CNC 모듈 임포트 실패: {e}")
    CNC_AVAILABLE = False

# CNC Subprocess Manager (32비트 호환성)
try:
    from backend.cnc_subprocess_manager import CNCSubprocessManager
    CNC_SUBPROCESS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"CNC Subprocess Manager 임포트 실패: {e}")
    CNC_SUBPROCESS_AVAILABLE = False

try:
    from Sensors.vision2 import HikCameraThread
    HIKCAMERA_AVAILABLE = True
except ImportError as e:
    logger.warning(f"HikRobot 카메라 모듈 임포트 실패: {e}")
    HIKCAMERA_AVAILABLE = False

# GuiState.ini 파일 리더 (피더 RPM, 가스 유량)
try:
    from gui_state_reader import GuiStateReader, get_gui_state_reader
    GUI_STATE_AVAILABLE = True
except ImportError as e:
    logger.warning(f"GuiState 리더 임포트 실패: {e}")
    GUI_STATE_AVAILABLE = False


class SensorManager:
    """
    센서 통신 및 데이터 수집을 관리하는 클래스
    
    GoF 패턴:
    - Factory Pattern: use_factory_pattern=True 시 SensorFactory 사용
    - Strategy Pattern: 센서별 통신 전략 자동 선택
    """
    
    def __init__(self, use_cnc_subprocess: bool = False, cnc_python_path: str = None, 
                 test_mode: bool = None, use_factory_pattern: bool = None):
        """
        Args:
            use_cnc_subprocess: True면 CNC를 subprocess로 실행 (32비트 호환성)
            cnc_python_path: 32비트 Python 실행 파일 경로
            test_mode: True면 센서 연결 없이 테스트 모드로 시작
            use_factory_pattern: True면 GoF Factory 패턴 사용 (환경변수: USE_FACTORY_PATTERN)
        """
        self.sensors = {}
        self.collectors = {}
        self.databases = {}
        self.connection_status = {}
        self.hik_cam_threads = {}
        self.use_cnc_subprocess = use_cnc_subprocess
        self.cnc_subprocess_manager = None
        
        # GoF Factory 패턴 사용 여부
        if use_factory_pattern is None:
            self.use_factory_pattern = os.getenv('USE_FACTORY_PATTERN', 'false').lower() == 'true'
        else:
            self.use_factory_pattern = use_factory_pattern
        
        # Factory 패턴 사용 시 새 센서 인스턴스 저장
        self._factory_sensors: Dict[str, 'ISensor'] = {}
        
        # GuiState.ini 리더 (피더 RPM, 가스 유량)
        self.gui_state_reader = None
        if GUI_STATE_AVAILABLE:
            self.gui_state_reader = get_gui_state_reader()
        
        # 테스트 모드 설정 (기본값: false - 실제 장비 연결)
        if test_mode is None:
            self.test_mode = os.getenv('TEST_MODE', 'false').lower() == 'true'
        else:
            self.test_mode = test_mode
        
        # 센서별 연결 상태
        self.connection_status = {
            "camera": False,
            "laser": False,
            "pyrometer": False,
            "cnc": False,
            "hik_camera_1": False,
            "hik_camera_2": False
        }
        
        # Factory 패턴 사용 로깅
        if self.use_factory_pattern and NEW_SENSORS_AVAILABLE:
            logger.info("🏭 GoF Factory 패턴 모드 활성화")
        elif self.use_factory_pattern and not NEW_SENSORS_AVAILABLE:
            logger.warning("⚠️ Factory 패턴 요청되었으나 모듈 미설치 - 레거시 모드 사용")
    
    async def initialize(self):
        """모든 센서 초기화 (백그라운드에서 진행, 서버는 즉시 시작)"""
        logger.info("센서 매니저 초기화 중...")
        
        # 테스트 모드에서는 센서 연결 건너뛰기
        if self.test_mode:
            logger.info("테스트 모드 활성화 - 센서 연결 건너뜀")
            return
        
        # 센서 초기화를 백그라운드에서 진행 (서버는 즉시 시작)
        logger.info("센서 연결을 백그라운드에서 진행합니다...")
        asyncio.create_task(self._initialize_sensors_background())
    
    async def _initialize_sensors_background(self):
        """백그라운드에서 센서 초기화 진행"""
        logger.info("백그라운드 센서 연결 시작...")
        
        # Factory 패턴 사용 시 새 방식으로 초기화
        if self.use_factory_pattern and NEW_SENSORS_AVAILABLE:
            await self._initialize_with_factory()
        else:
            # 레거시 방식: 각 센서를 비동기적으로 초기화
            await asyncio.gather(
                self._initialize_camera(),      # Basler 카메라
                self._initialize_laser(),       # IPG 레이저
                self._initialize_pyrometer(),   # Pyrometer
                self._initialize_cnc(),         # CNC
                # self._initialize_hik_cameras(),  # HikRobot 카메라 - 비활성화
                return_exceptions=True
            )
        
        # 연결 상태 출력
        connected = [k for k, v in self.connection_status.items() if v]
        disconnected = [k for k, v in self.connection_status.items() if not v]
        
        if connected:
            logger.info(f"연결된 센서: {', '.join(connected)}")
        if disconnected:
            logger.info(f"연결 안됨: {', '.join(disconnected)}")
            logger.info(
                "일부 센서 미연결 시: trouble_shooting_md/SENSOR_CONNECTION_ERRORS_KR.md 참고 "
                "(Basler=다른 프로그램 종료, COM=포트 사용 중인 프로그램 확인, 레이저/CNC=전원·IP 확인)"
            )
        
        logger.info("백그라운드 센서 연결 완료")
    
    async def _initialize_with_factory(self):
        """
        Factory 패턴을 사용한 센서 초기화
        
        GoF Pattern:
        - Factory Pattern: SensorFactory.create()로 센서 생성
        - Template Method: BaseSensor.connect()로 연결
        
        Note: 카메라는 레거시 방식 사용 (CameraDB/CameraCollector 필요)
        """
        logger.info("🏭 Factory 패턴으로 센서 초기화 중...")
        
        # 카메라는 레거시 방식으로 초기화 (CameraDB/CameraCollector 필요)
        if CAMERA_AVAILABLE:
            await self._initialize_camera()
        
        # 나머지 센서는 Factory 패턴으로 초기화
        sensor_types = ['laser', 'pyrometer', 'cnc']
        
        for sensor_type in sensor_types:
            try:
                # Factory를 통해 센서 생성
                sensor = SensorFactory.create_safe(sensor_type)
                
                if sensor is None:
                    logger.warning(f"[{sensor_type}] 센서 생성 실패")
                    self.connection_status[sensor_type] = False
                    continue
                
                # 비동기로 연결 시도 (CNC는 HXApi 준비 지연으로 10초, 나머지 3초)
                loop = asyncio.get_event_loop()
                timeout_sec = 10.0 if sensor_type == "cnc" else 3.0
                try:
                    connected = await asyncio.wait_for(
                        loop.run_in_executor(None, sensor.connect),
                        timeout=timeout_sec
                    )
                    
                    if connected:
                        self._factory_sensors[sensor_type] = sensor
                        self.connection_status[sensor_type] = True
                        logger.info(f"✅ [{sensor_type}] 연결 성공 (Factory)")
                    else:
                        self.connection_status[sensor_type] = False
                        logger.warning(f"❌ [{sensor_type}] 연결 실패")
                        
                except asyncio.TimeoutError:
                    self.connection_status[sensor_type] = False
                    logger.warning(f"⏱️ [{sensor_type}] 연결 타임아웃")
                    
            except Exception as e:
                self.connection_status[sensor_type] = False
                logger.error(f"❌ [{sensor_type}] 초기화 오류: {e}")
        
        logger.info("🏭 Factory 패턴 센서 초기화 완료")
    
    async def _initialize_camera(self):
        """Basler 카메라 초기화 (3초 타임아웃)"""
        if not CAMERA_AVAILABLE:
            logger.warning("카메라 모듈이 사용 불가능합니다")
            self.connection_status["camera"] = False
            return
            
        try:
            logger.info("Basler 카메라 연결 시도 중...")
            
            loop = asyncio.get_event_loop()
            
            try:
                self.sensors["camera"] = await asyncio.wait_for(
                    loop.run_in_executor(None, CameraCommunication),
                    timeout=3.0
                )
                self.databases["camera"] = CameraDB()
                self.collectors["camera"] = CameraCollector(
                    self.sensors["camera"], 
                    self.databases["camera"]
                )
                
                self.collectors["camera"].start()
                self.connection_status["camera"] = True
                
                logger.info("Basler 카메라 연결 성공")
            except asyncio.TimeoutError:
                logger.warning("Basler 카메라 연결 타임아웃 (3초 초과)")
                self.connection_status["camera"] = False
            
        except Exception as e:
            logger.error(f"Basler 카메라 연결 실패: {e}")
            self.connection_status["camera"] = False
    
    async def _initialize_laser(self):
        """IPG 레이저 초기화 (3초 타임아웃)"""
        if not LASER_AVAILABLE:
            logger.warning("레이저 모듈이 사용 불가능합니다")
            self.connection_status["laser"] = False
            return
            
        try:
            logger.info("IPG 레이저 연결 시도 중...")
            
            loop = asyncio.get_event_loop()
            
            try:
                self.sensors["laser"] = await asyncio.wait_for(
                    loop.run_in_executor(None, LaserCommunication),
                    timeout=3.0
                )
                self.databases["laser"] = LaserDB()
                self.collectors["laser"] = IPG_Collector(
                    self.sensors["laser"],
                    self.databases["laser"]
                )
                
                self.collectors["laser"].start()
                self.connection_status["laser"] = True
                
                logger.info("IPG 레이저 연결 성공")
            except asyncio.TimeoutError:
                logger.warning("IPG 레이저 연결 타임아웃 (3초 초과)")
                self.connection_status["laser"] = False
            
        except Exception as e:
            logger.error(f"IPG 레이저 연결 실패: {e}")
            self.connection_status["laser"] = False
    
    async def _initialize_pyrometer(self):
        """Pyrometer 초기화 (3초 타임아웃)"""
        if not PYROMETER_AVAILABLE:
            logger.warning("Pyrometer 모듈이 사용 불가능합니다")
            self.connection_status["pyrometer"] = False
            return
            
        try:
            logger.info("Pyrometer 연결 시도 중...")
            
            loop = asyncio.get_event_loop()
            
            try:
                self.sensors["pyrometer"] = await asyncio.wait_for(
                    loop.run_in_executor(None, PyrometerCommunication),
                    timeout=3.0
                )
                self.databases["pyrometer"] = PyrometerDB()
                self.collectors["pyrometer"] = PyrometerCollector(
                    self.sensors["pyrometer"],
                    self.databases["pyrometer"]
                )
                
                self.collectors["pyrometer"].start()
                self.connection_status["pyrometer"] = True
                
                logger.info("Pyrometer 연결 성공")
            except asyncio.TimeoutError:
                logger.warning("Pyrometer 연결 타임아웃 (3초 초과)")
                self.connection_status["pyrometer"] = False
            
        except Exception as e:
            logger.error(f"Pyrometer 연결 실패: {e}")
            self.connection_status["pyrometer"] = False
    
    async def _initialize_cnc(self):
        """HXApi CNC 초기화 (subprocess 옵션 지원)"""
        # Subprocess 모드 사용
        if self.use_cnc_subprocess:
            if not CNC_SUBPROCESS_AVAILABLE:
                logger.warning("CNC Subprocess Manager가 사용 불가능합니다")
                self.connection_status["cnc"] = False
                return
            
            try:
                logger.info("HXApi CNC 연결 시도 중... (Subprocess 모드)")
                
                config_path = os.path.join(
                    os.path.dirname(os.path.dirname(__file__)),
                    "config", "HXApi.ini"
                )
                
                cnc_python_path = os.getenv('CNC_PYTHON_EXECUTABLE', None)
                
                self.cnc_subprocess_manager = CNCSubprocessManager(
                    python_executable=cnc_python_path,
                    config_path=config_path
                )
                self.cnc_subprocess_manager.start()
                
                self.databases["cnc"] = None
                self.connection_status["cnc"] = True
                
                logger.info("HXApi CNC 연결 성공 (Subprocess 모드)")
                
            except Exception as e:
                logger.error(f"HXApi CNC 연결 실패 (Subprocess): {e}")
                self.connection_status["cnc"] = False
                return
        
        # 직접 DLL 로드 모드 (기존 방식)
        else:
            if not CNC_AVAILABLE:
                logger.warning("CNC 모듈이 사용 불가능합니다")
                self.connection_status["cnc"] = False
                return
                
            try:
                logger.info("HXApi CNC 연결 시도 중... (직접 DLL 로드)")
                
                loop = asyncio.get_event_loop()
                
                config_path = os.path.join(
                    os.path.dirname(os.path.dirname(__file__)),
                    "config", "HXApi.ini"
                )
                
                try:
                    self.sensors["cnc"] = await asyncio.wait_for(
                        loop.run_in_executor(None, CNCCommunication, config_path),
                        timeout=15.0  # CNC 연결은 더 오래 걸릴 수 있음
                    )
                    self.databases["cnc"] = CNC_DB()
                    self.collectors["cnc"] = CNC_Collector(
                        self.sensors["cnc"],
                        self.databases["cnc"]
                    )
                    
                    self.collectors["cnc"].start()
                    self.connection_status["cnc"] = True
                    
                    logger.info("HXApi CNC 연결 성공 (직접 DLL 로드)")
                except asyncio.TimeoutError:
                    logger.warning("HXApi CNC 연결 타임아웃 (5초 초과)")
                    self.connection_status["cnc"] = False
                
            except Exception as e:
                logger.error(f"HXApi CNC 연결 실패: {e}")
                self.connection_status["cnc"] = False
    
    async def _initialize_hik_cameras(self):
        """HikRobot 카메라 2대 초기화 (3초 타임아웃)"""
        if not HIKCAMERA_AVAILABLE:
            logger.warning("HikRobot 카메라 모듈이 사용 불가능합니다")
            self.connection_status["hik_camera_1"] = False
            self.connection_status["hik_camera_2"] = False
            return
            
        try:
            logger.info("HikRobot 카메라 연결 시도 중...")
            
            loop = asyncio.get_event_loop()
            
            def push_hik_frame_1(frame):
                self.latest_frame1 = frame
            
            def push_hik_frame_2(frame):
                self.latest_frame2 = frame
            
            try:
                def init_hik_cameras():
                    cam1 = HikCameraThread(
                        "02J81094725", 
                        on_new_frame=push_hik_frame_1, 
                        parent=self
                    )
                    cam1.start()
                    
                    cam2 = HikCameraThread(
                        "02J75405689", 
                        on_new_frame=push_hik_frame_2, 
                        parent=self
                    )
                    cam2.start()
                    return cam1, cam2
                
                cam1, cam2 = await asyncio.wait_for(
                    loop.run_in_executor(None, init_hik_cameras),
                    timeout=3.0
                )
                
                self.hik_cam_threads["hik_camera_1"] = cam1
                self.hik_cam_threads["hik_camera_2"] = cam2
                self.connection_status["hik_camera_1"] = True
                self.connection_status["hik_camera_2"] = True
                
                self.latest_frame1 = None
                self.latest_frame2 = None
                
                logger.info("HikRobot 카메라 연결 성공")
            except asyncio.TimeoutError:
                logger.warning("HikRobot 카메라 연결 타임아웃 (3초 초과)")
                self.connection_status["hik_camera_1"] = False
                self.connection_status["hik_camera_2"] = False
            
        except Exception as e:
            logger.error(f"HikRobot 카메라 연결 실패: {e}")
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
        
        # 각 센서 DB에서 최신 데이터 조회
        loop = asyncio.get_event_loop()
        
        # Factory 패턴 사용 시 새 센서에서 데이터 수집
        if self.use_factory_pattern and self._factory_sensors:
            sensor_data = await self._collect_from_factory_sensors(sensor_data, loop)
        else:
            # 레거시 방식: 기존 DB에서 데이터 조회
            sensor_data = await self._collect_from_legacy_sensors(sensor_data, loop)
        
        return sensor_data
    
    async def _collect_from_factory_sensors(self, sensor_data: Dict, loop) -> Dict:
        """Factory 패턴 센서에서 데이터 수집"""
        
        # 카메라 데이터
        if 'camera' in self._factory_sensors:
            try:
                camera_data = await loop.run_in_executor(
                    None, self._factory_sensors['camera'].get_data
                )
                if camera_data:
                    sensor_data["camera_data"] = {
                        "melt_pool_area": camera_data.get("melt_pool_area", 0),
                        "image_available": camera_data.get("image") is not None
                    }
            except Exception as e:
                logger.warning(f"카메라 데이터 수집 오류: {e}")
        
        # 레이저 데이터
        if 'laser' in self._factory_sensors:
            try:
                laser_data = await loop.run_in_executor(
                    None, self._factory_sensors['laser'].get_data
                )
                if laser_data:
                    sensor_data["laser_data"] = laser_data
            except Exception as e:
                logger.warning(f"레이저 데이터 수집 오류: {e}")
        
        # Pyrometer 데이터
        if 'pyrometer' in self._factory_sensors:
            try:
                pyrometer_data = await loop.run_in_executor(
                    None, self._factory_sensors['pyrometer'].get_data
                )
                if pyrometer_data:
                    sensor_data["pyrometer_data"] = pyrometer_data
            except Exception as e:
                logger.warning(f"Pyrometer 데이터 수집 오류: {e}")
        
        # CNC 데이터
        if 'cnc' in self._factory_sensors:
            try:
                cnc_data = await loop.run_in_executor(
                    None, self._factory_sensors['cnc'].get_data
                )
                if cnc_data:
                    # GuiState.ini에서 피더 RPM, 가스 유량 읽어서 병합
                    if self.gui_state_reader:
                        gui_data = self.gui_state_reader.read()
                        cnc_data.update(gui_data.to_dict())
                    
                    sensor_data["cnc_data"] = cnc_data
            except Exception as e:
                logger.warning(f"CNC 데이터 수집 오류: {e}")
        
        # HikRobot 카메라 (레거시 유지)
        if (self.connection_status["hik_camera_1"] and 
            self.connection_status["hik_camera_2"]):
            try:
                hik_data = self._get_combined_hik_image()
                if hik_data:
                    sensor_data["hik_camera_data"] = hik_data
            except Exception as e:
                logger.warning(f"HikRobot 데이터 수집 오류: {e}")
        
        return sensor_data
    
    async def _collect_from_legacy_sensors(self, sensor_data: Dict, loop) -> Dict:
        """레거시 센서에서 데이터 수집"""
        
        # 카메라 데이터
        if self.connection_status["camera"] and "camera" in self.databases:
            try:
                camera_data = await loop.run_in_executor(
                    None, self.databases["camera"].retrieve_data
                )
                if camera_data:
                    sensor_data["camera_data"] = {
                        "melt_pool_area": camera_data.get("melt_pool_area", 0),
                        "image_available": camera_data.get("image") is not None
                    }
            except Exception as e:
                logger.warning(f"카메라 데이터 수집 오류: {e}")
        
        # 레이저 데이터
        if self.connection_status["laser"] and "laser" in self.databases:
            try:
                laser_data = await loop.run_in_executor(
                    None, self.databases["laser"].retrieve_data
                )
                if laser_data:
                    sensor_data["laser_data"] = laser_data
            except Exception as e:
                logger.warning(f"레이저 데이터 수집 오류: {e}")
        
        # Pyrometer 데이터
        if self.connection_status["pyrometer"] and "pyrometer" in self.databases:
            try:
                pyrometer_data = await loop.run_in_executor(
                    None, self.databases["pyrometer"].retrieve_data
                )
                if pyrometer_data:
                    sensor_data["pyrometer_data"] = pyrometer_data
            except Exception as e:
                logger.warning(f"Pyrometer 데이터 수집 오류: {e}")
        
        # CNC 데이터
        if self.connection_status["cnc"]:
            try:
                cnc_data = None
                if self.use_cnc_subprocess and self.cnc_subprocess_manager:
                    cnc_data = self.cnc_subprocess_manager.get_latest_data()
                elif "cnc" in self.databases and self.databases["cnc"]:
                    cnc_data = await loop.run_in_executor(
                        None, self.databases["cnc"].retrieve_data
                    )
                
                if cnc_data:
                    # GuiState.ini에서 피더 RPM, 가스 유량 읽어서 병합
                    if self.gui_state_reader:
                        gui_data = self.gui_state_reader.read()
                        cnc_data.update(gui_data.to_dict())
                    
                    sensor_data["cnc_data"] = cnc_data
            except Exception as e:
                logger.warning(f"CNC 데이터 수집 오류: {e}")
        
        # HikRobot 카메라 데이터
        if (self.connection_status["hik_camera_1"] and 
            self.connection_status["hik_camera_2"]):
            try:
                hik_data = self._get_combined_hik_image()
                if hik_data:
                    sensor_data["hik_camera_data"] = hik_data
            except Exception as e:
                logger.warning(f"HikRobot 데이터 수집 오류: {e}")
        
        return sensor_data
    
    def _get_combined_hik_image(self) -> Optional[Dict]:
        """HikRobot 2대 이미지를 합쳐서 반환"""
        if not self.connection_status.get("hik_camera_1") or not self.connection_status.get("hik_camera_2"):
            return None
        
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
                    logger.warning(f"HikRobot 이미지 합치기 오류: {e}")
        return None
    
    async def get_connection_status(self) -> Dict[str, bool]:
        """연결 상태 조회"""
        return self.connection_status.copy()
    
    async def cleanup(self):
        """리소스 정리"""
        logger.info("센서 매니저 정리 중...")
        
        # CNC Subprocess 정지
        if self.cnc_subprocess_manager:
            try:
                self.cnc_subprocess_manager.stop()
                logger.info("CNC subprocess 정지 완료")
            except Exception as e:
                logger.warning(f"CNC subprocess 정지 오류: {e}")
        
        # 모든 컬렉터 정지
        for name, collector in self.collectors.items():
            try:
                collector.stop()
                collector.join(timeout=5)
                logger.info(f"{name} 컬렉터 정지 완료")
            except Exception as e:
                logger.warning(f"{name} 컬렉터 정지 오류: {e}")
        
        # HikRobot 카메라 정지
        for name, thread in self.hik_cam_threads.items():
            try:
                thread.stop()
                thread.join(timeout=5)
                logger.info(f"{name} 스레드 정지 완료")
            except Exception as e:
                logger.warning(f"{name} 스레드 정지 오류: {e}")
        
        # 레거시 센서 연결 종료
        for name, sensor in self.sensors.items():
            try:
                if hasattr(sensor, 'close'):
                    sensor.close()
                logger.info(f"{name} 센서 연결 종료 완료")
            except Exception as e:
                logger.warning(f"{name} 센서 연결 종료 오류: {e}")
        
        # Factory 패턴 센서 연결 종료
        for name, sensor in self._factory_sensors.items():
            try:
                sensor.disconnect()
                logger.info(f"{name} 센서 (Factory) 연결 종료 완료")
            except Exception as e:
                logger.warning(f"{name} 센서 (Factory) 연결 종료 오류: {e}")
        
        self._factory_sensors.clear()
        
        logger.info("센서 매니저 정리 완료")
