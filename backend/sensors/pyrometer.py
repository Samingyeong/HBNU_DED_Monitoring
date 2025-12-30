"""
파이로미터 센서 (2-Color Pyrometer)
===================================

역할:
- 2-Color Pyrometer 연결 및 온도 데이터 수집
- MPT, 1CT, 2CT 온도 읽기

통신 방식:
- Serial 통신 (RS-232)
"""
import os
import sys
import configparser
import logging
from typing import Dict, Any, Optional

from .base import BaseSensor
from .factory import register_sensor

logger = logging.getLogger("HBNU_Backend")

# pyserial 임포트 (선택적)
try:
    import serial
    SERIAL_AVAILABLE = True
except ImportError:
    SERIAL_AVAILABLE = False
    logger.warning("pyserial 모듈을 찾을 수 없습니다. Pyrometer 기능이 비활성화됩니다.")

# 기본 설정 파일 경로
DEFAULT_CONFIG_PATH = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "../../config/Pyrometer.ini")
)


@register_sensor('pyrometer', default_config=DEFAULT_CONFIG_PATH)
class PyrometerSensor(BaseSensor):
    """
    2-Color Pyrometer 센서
    
    기능:
    - Serial 연결
    - MPT (Main Pyrometer Temperature) 읽기
    - 1CT, 2CT (Color Temperature) 읽기
    """
    
    def __init__(self, config_path: Optional[str] = None):
        config_path = config_path or DEFAULT_CONFIG_PATH
        super().__init__(config_path=config_path, name="2-Color Pyrometer")
        
        self._serial: Optional['serial.Serial'] = None
        self._port: str = ""
        self._baudrate: int = 9600
        self._parity: str = 'N'
        self._stopbits: int = 1
        self._bytesize: int = 8
        self._timeout: int = 1
        
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
            self._port = config.get('address', 'port', fallback='COM12')
            self._baudrate = config.getint('address', 'baudrate', fallback=9600)
            self._parity = config.get('address', 'parity', fallback='N')
            self._stopbits = config.getint('address', 'stopbits', fallback=1)
            self._bytesize = config.getint('address', 'bytesize', fallback=8)
            self._timeout = config.getint('address', 'timeout', fallback=1)
        
        logger.debug(f"[{self._name}] 설정 로드: {self._port} @ {self._baudrate}")
    
    def _do_connect(self) -> None:
        """Serial 연결"""
        if not SERIAL_AVAILABLE:
            raise RuntimeError("pyserial 모듈이 설치되지 않았습니다")
        
        if not self._port:
            raise RuntimeError("포트가 설정되지 않았습니다")
        
        self._serial = serial.Serial(
            port=self._port,
            baudrate=self._baudrate,
            parity=self._parity,
            stopbits=self._stopbits,
            bytesize=self._bytesize,
            timeout=self._timeout
        )
        
        if not self._serial.is_open:
            raise RuntimeError(f"포트 열기 실패: {self._port}")
        
        # 초기 연결 확인
        self._serial.write("00bum01\r".encode('ascii'))
        response = self._serial.read_until(b'\r').decode('utf-8').strip()
        
        if response != 'ok':
            raise RuntimeError(f"Pyrometer 응답 오류: {response}")
        
        logger.info(f"[{self._name}] 연결됨: {self._port}")
    
    def _do_disconnect(self) -> None:
        """Serial 연결 해제"""
        if self._serial and self._serial.is_open:
            self._serial.close()
        self._serial = None
    
    def _do_get_data(self) -> Dict[str, Any]:
        """온도 데이터 수집"""
        if self._serial is None or not self._serial.is_open:
            return {"mpt": None, "1ct": None, "2ct": None}
        
        try:
            # 버퍼 클리어 (데이터 깨짐 방지)
            self._serial.reset_input_buffer()
            self._serial.write("00bup\r".encode('ascii'))
            
            response = self._read_valid_response()
            
            if response:
                return self._parse_temperature(response)
            
        except Exception as e:
            logger.warning(f"[{self._name}] 데이터 읽기 실패: {e}")
        
        return {"mpt": None, "1ct": None, "2ct": None}
    
    def _read_valid_response(self, max_attempts: int = 3) -> Optional[str]:
        """유효한 응답 읽기 (재시도 포함)"""
        for _ in range(max_attempts):
            try:
                candidate = self._serial.read_until(b'\r').decode('utf-8').strip()
                
                # 유효성 검사: 12자리 16진수
                if len(candidate) == 12 and all(
                    c in "0123456789ABCDEFabcdef" for c in candidate
                ):
                    return candidate
                    
            except Exception:
                continue
        
        return None
    
    def _parse_temperature(self, response: str) -> Dict[str, Any]:
        """온도 데이터 파싱"""
        try:
            mpt = int(response[0:4], 16) / 10
            c1 = int(response[4:8], 16) / 10
            c2 = int(response[8:12], 16) / 10
            
            return {
                "mpt": mpt,
                "1ct": c1,
                "2ct": c2
            }
        except (ValueError, IndexError) as e:
            logger.warning(f"[{self._name}] 파싱 오류: {e}")
            return {"mpt": None, "1ct": None, "2ct": None}
