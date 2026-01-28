"""
CNC 센서 (HXAPI)
================

역할:
- CNC 좌표 데이터 수집 (현재좌표, 기계좌표, 잔여좌표)
- Feed Rate, Override 데이터 읽기

통신 방식:~
- DLL 호출 (HXApi.dll)
"""
import os
import sys
import ctypes
import configparser
import logging
from typing import Dict, Any, Optional

from .base import BaseSensor
from .factory import register_sensor

logger = logging.getLogger("HBNU_Backend")

# DLL 경로 설정
SENSORS_PATH = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "../../Sensors")
)
DLL_PATH = os.path.join(SENSORS_PATH, "HXApi", "dll")

# PATH에 DLL 경로 추가
if os.path.exists(DLL_PATH):
    os.environ['PATH'] = DLL_PATH + os.pathsep + os.environ['PATH']

# 기본 설정 파일 경로
DEFAULT_CONFIG_PATH = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "../../config/HXApi.ini")
)


@register_sensor('cnc', default_config=DEFAULT_CONFIG_PATH)
class CnCSensor(BaseSensor):
    """
    CNC 센서 (HXAPI)
    
    기능:
    - DLL 연결 (HXApi.dll)
    - 좌표 데이터 읽기 (curpos, macpos, rempos)
    - Feed Rate, Override 읽기
    """
    
    def __init__(self, config_path: Optional[str] = None):
        config_path = config_path or DEFAULT_CONFIG_PATH
        super().__init__(config_path=config_path, name="CNC (HXAPI)")
        
        self._hx = None
        self._ip: str = "127.0.0.1"
        self._port: int = 3000
        
        # 설정 파일 로드
        self._load_config()
    
    def _load_config(self) -> None:
        """설정 파일 로드"""
        if not self._config_path or not os.path.exists(self._config_path):
            logger.warning(f"[{self._name}] 설정 파일 없음: {self._config_path}")
            return
        
        config = configparser.ConfigParser()
        config.read(self._config_path)
        
        if config.has_section('address'):
            self._ip = config.get('address', 'ip', fallback='127.0.0.1')
            self._port = config.getint('address', 'port', fallback=3000)
        
        logger.debug(f"[{self._name}] 설정 로드: {self._ip}:{self._port}")
    
    def _do_connect(self) -> None:
        """HXApi DLL 연결"""
        dll_file = os.path.join(DLL_PATH, "HXApi.dll")
        
        if not os.path.exists(dll_file):
            raise RuntimeError(f"DLL 파일 없음: {dll_file}")
        
        try:
            self._hx = ctypes.CDLL(dll_file)
        except OSError as e:
            raise RuntimeError(f"DLL 로드 실패: {e}")
        
        # API 함수 타입 설정
        self._setup_api_types()
        
        # 연결
        ip_parts = self._ip.split('.')
        if len(ip_parts) != 4:
            raise RuntimeError(f"잘못된 IP 주소: {self._ip}")
        
        result = self._hx.HxInitialize2(
            0,
            int(ip_parts[0]),
            int(ip_parts[1]),
            int(ip_parts[2]),
            int(ip_parts[3]),
            self._port
        )
        
        if not result:
            raise RuntimeError("HxInitialize2 실패")
        
        logger.info(f"[{self._name}] 연결됨: {self._ip}:{self._port}")
    
    def _setup_api_types(self) -> None:
        """API 함수 타입 설정"""
        # HxInitialize2
        self._hx.HxInitialize2.argtypes = [
            ctypes.c_int32, ctypes.c_int32, ctypes.c_int32,
            ctypes.c_int32, ctypes.c_int32, ctypes.c_int32
        ]
        self._hx.HxInitialize2.restype = ctypes.c_bool
        
        # HxGetSVF (System Variable Float)
        self._hx.HxGetSVF.argtypes = [ctypes.c_int32, ctypes.c_int32]
        self._hx.HxGetSVF.restype = ctypes.c_double
        
        # HxGetSNF (System Number Float)
        self._hx.HxGetSNF.argtypes = [ctypes.c_int32, ctypes.c_int32]
        self._hx.HxGetSNF.restype = ctypes.c_double
        
        # HxGetRW (R Register Word)
        self._hx.HxGetRW.argtypes = [ctypes.c_int32, ctypes.c_int32]
        self._hx.HxGetRW.restype = ctypes.c_int32
        
        # HxGetRB (R Register Bit)
        self._hx.HxGetRB.argtypes = [ctypes.c_int32, ctypes.c_int32, ctypes.c_int32]
        self._hx.HxGetRB.restype = ctypes.c_bool
        # HxGetSystemEmg (비상정지, Hx20Api 등에 있음. 없으면 무시)
        try:
            if hasattr(self._hx, 'HxGetSystemEmg'):
                self._hx.HxGetSystemEmg.argtypes = [ctypes.c_int32]
                self._hx.HxGetSystemEmg.restype = ctypes.c_bool
        except Exception:
            pass

    def _do_disconnect(self) -> None:
        """DLL 연결 해제"""
        self._hx = None
    
    def _do_get_data(self) -> Dict[str, Any]:
        """CNC 좌표 데이터 수집"""
        if self._hx is None:
            return {}
        
        try:
            data = {
                # 현재 좌표
                'curpos_x': self._hx.HxGetSVF(0, 83),
                'curpos_y': self._hx.HxGetSVF(0, 84),
                'curpos_z': self._hx.HxGetSVF(0, 85),
                'curpos_a': self._hx.HxGetSVF(0, 86),
                'curpos_c': self._hx.HxGetSVF(0, 87),
                
                # 기계 좌표
                'macpos_x': self._hx.HxGetSNF(0, 237),
                'macpos_y': self._hx.HxGetSNF(0, 238),
                'macpos_z': self._hx.HxGetSNF(0, 239),
                'macpos_a': self._hx.HxGetSNF(0, 240),
                'macpos_c': self._hx.HxGetSNF(0, 241),
                
                # 잔여 좌표
                'rempos_x': self._hx.HxGetSNF(0, 247),
                'rempos_y': self._hx.HxGetSNF(0, 248),
                'rempos_z': self._hx.HxGetSNF(0, 249),
                'rempos_a': self._hx.HxGetSNF(0, 250),
                'rempos_c': self._hx.HxGetSNF(0, 251),
                
                # 운전 시간
                'oper_time': self._hx.HxGetSNF(0, 0),
                'total_oper_time': self._hx.HxGetSNF(0, 1),
                
                # Override
                'feed_override': self._hx.HxGetSVF(0, 675),
                'rapid_override': self._hx.HxGetSVF(0, 676),
                'feed_rate': self._hx.HxGetSVF(0, 722),
            }
            # 비상정지(E-STOP): HxGetSystemEmg 지원 시 사용
            try:
                if hasattr(self._hx, 'HxGetSystemEmg'):
                    data['estop'] = bool(self._hx.HxGetSystemEmg(0))
                else:
                    data['estop'] = False
            except Exception:
                data['estop'] = False

            return data
            
        except Exception as e:
            logger.warning(f"[{self._name}] 데이터 읽기 실패: {e}")
            return {}
