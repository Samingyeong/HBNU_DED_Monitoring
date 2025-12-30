"""
레이저 센서 (IPG Laser)
=======================

역할:
- IPG 레이저 연결 및 데이터 수집
- 출력 파워, 설정 파워 읽기

통신 방식:
- TCP Socket 통신
"""
import os
import sys
import socket
import configparser
import logging
from typing import Dict, Any, Optional

from .base import BaseSensor
from .factory import register_sensor

logger = logging.getLogger("HBNU_Backend")

# 기본 설정 파일 경로
DEFAULT_CONFIG_PATH = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "../../config/IPG.ini")
)


@register_sensor('laser', default_config=DEFAULT_CONFIG_PATH)
class LaserSensor(BaseSensor):
    """
    IPG 레이저 센서
    
    기능:
    - TCP 소켓 연결
    - 출력 파워 (ROP) 읽기
    - 설정 파워 (RCS) 읽기
    """
    
    def __init__(self, config_path: Optional[str] = None):
        config_path = config_path or DEFAULT_CONFIG_PATH
        super().__init__(config_path=config_path, name="IPG Laser")
        
        self._socket: Optional[socket.socket] = None
        self._ip: str = ""
        self._port: int = 0
        
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
            self._port = config.getint('address', 'port', fallback=10001)
        
        logger.debug(f"[{self._name}] 설정 로드: {self._ip}:{self._port}")
    
    def _do_connect(self) -> None:
        """TCP 소켓 연결"""
        if not self._ip or not self._port:
            raise RuntimeError("IP 또는 포트가 설정되지 않았습니다")
        
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(5.0)
        
        try:
            self._socket.connect((self._ip, self._port))
            logger.info(f"[{self._name}] 연결됨: {self._ip}:{self._port}")
        except Exception as e:
            self._socket = None
            raise RuntimeError(f"연결 실패: {e}")
    
    def _do_disconnect(self) -> None:
        """소켓 연결 해제"""
        if self._socket:
            try:
                self._socket.close()
            except Exception:
                pass
            self._socket = None
    
    def _do_get_data(self) -> Dict[str, Any]:
        """레이저 데이터 수집"""
        if self._socket is None:
            return {"outpower": None, "setpower": None}
        
        outpower = self._read_outpower()
        setpower = self._read_setpower()
        
        return {
            "outpower": outpower,
            "setpower": setpower
        }
    
    def _read_outpower(self) -> Optional[float]:
        """출력 파워 읽기 (ROP 명령)"""
        try:
            self._socket.sendall("ROP\r".encode('ascii'))
            response = self._socket.recv(1024).decode('ascii').strip()
            
            outpower_str = response.split(':')[-1].strip()
            
            if outpower_str.lower() in ('off', 'low'):
                return 0.0
            
            return float(outpower_str)
            
        except Exception as e:
            logger.warning(f"[{self._name}] ROP 읽기 실패: {e}")
            return None
    
    def _read_setpower(self) -> Optional[float]:
        """설정 파워 읽기 (RCS 명령)"""
        try:
            self._socket.sendall("RCS\r".encode('ascii'))
            response = self._socket.recv(1024).decode('ascii').strip()
            
            setpower_str = response.split(':')[-1].strip()
            return float(setpower_str)
            
        except Exception as e:
            logger.warning(f"[{self._name}] RCS 읽기 실패: {e}")
            return None
