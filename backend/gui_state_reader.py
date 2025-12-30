"""
DED GuiState.ini 파일 읽기 모듈
================================

역할:
- C:\DED\CS3AXIS\Data\GuiState.ini 또는 C:\DED\CS5AXIS\Data\GuiState.ini 파일에서
  피더 RPM, 가스 유량 데이터를 읽어옴
- CNC R 레지스터가 아닌 실제 DED 시스템의 피더/가스 상태 반영
"""
import os
import configparser
import logging
from typing import Dict, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class FeederGasData:
    """피더 및 가스 데이터"""
    # 피더 RPM
    feeder1_rpm: int = 0
    feeder2_rpm: int = 0
    feeder3_rpm: int = 0
    feeder4_rpm: int = 0
    feeder5_rpm: int = 0
    feeder6_rpm: int = 0
    
    # 가스 유량
    powder_gas: float = 0.0
    coaxial_gas: float = 0.0
    shield_gas: float = 0.0
    
    # 레이저 파워 (JOG 모드)
    laser_power: int = 0
    
    def to_dict(self) -> Dict:
        return {
            "feeder1_rpm": self.feeder1_rpm,
            "feeder2_rpm": self.feeder2_rpm,
            "feeder3_rpm": self.feeder3_rpm,
            "feeder4_rpm": self.feeder4_rpm,
            "feeder5_rpm": self.feeder5_rpm,
            "feeder6_rpm": self.feeder6_rpm,
            "powder_gas": self.powder_gas,
            "coaxial_gas": self.coaxial_gas,
            "shield_gas": self.shield_gas,
            "laser_power_jog": self.laser_power
        }


class GuiStateReader:
    """
    DED GuiState.ini 파일 리더
    
    - CS5AXIS 우선, 없으면 CS3AXIS 폴더에서 읽기
    - 파일이 없으면 빈 데이터 반환 (더미 데이터 없음)
    """
    
    # GuiState.ini 파일 경로 (우선순위)
    GUI_STATE_PATHS = [
        r'C:\DED\CS5AXIS\Data\GuiState.ini',
        r'C:\DED\CS3AXIS\Data\GuiState.ini',
        r'D:\DED\CS5AXIS\Data\GuiState.ini',
        r'D:\DED\CS3AXIS\Data\GuiState.ini',
    ]
    
    def __init__(self):
        self._config = configparser.ConfigParser()
        self._current_path: Optional[str] = None
        self._last_data = FeederGasData()
        self._find_gui_state_file()
    
    def _find_gui_state_file(self):
        """GuiState.ini 파일 찾기"""
        for path in self.GUI_STATE_PATHS:
            if os.path.exists(path):
                self._current_path = path
                logger.info(f"✅ GuiState.ini 파일 발견: {path}")
                return
        
        logger.warning("⚠️ GuiState.ini 파일을 찾을 수 없습니다")
        self._current_path = None
    
    def read(self) -> FeederGasData:
        """GuiState.ini에서 피더/가스 데이터 읽기"""
        if not self._current_path or not os.path.exists(self._current_path):
            # 파일 다시 찾기 시도
            self._find_gui_state_file()
            if not self._current_path:
                return FeederGasData()  # 빈 데이터 반환
        
        try:
            # 파일 읽기 (다양한 인코딩 시도)
            for encoding in ['utf-8', 'cp949', 'euc-kr', 'latin-1']:
                try:
                    self._config.read(self._current_path, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            
            data = FeederGasData()
            
            # [JOG_WINDOW] 섹션에서 데이터 읽기
            if self._config.has_section('JOG_WINDOW'):
                # 피더 RPM
                data.feeder1_rpm = self._get_int('JOG_WINDOW', 'Feeder1', 0)
                data.feeder2_rpm = self._get_int('JOG_WINDOW', 'Feeder2', 0)
                data.feeder3_rpm = self._get_int('JOG_WINDOW', 'Feeder3', 0)
                data.feeder4_rpm = self._get_int('JOG_WINDOW', 'Feeder4', 0)
                data.feeder5_rpm = self._get_int('JOG_WINDOW', 'Feeder5', 0)
                data.feeder6_rpm = self._get_int('JOG_WINDOW', 'Feeder6', 0)
                
                # 가스 유량
                data.powder_gas = self._get_float('JOG_WINDOW', 'PowderGas', 0.0)
                data.coaxial_gas = self._get_float('JOG_WINDOW', 'CoaxialGas', 0.0)
                data.shield_gas = self._get_float('JOG_WINDOW', 'ShieldGas', 0.0)
                
                # 레이저 파워
                data.laser_power = self._get_int('JOG_WINDOW', 'LaserPower', 0)
            
            self._last_data = data
            return data
            
        except Exception as e:
            logger.error(f"❌ GuiState.ini 읽기 오류: {e}")
            return self._last_data  # 마지막 성공 데이터 반환
    
    def _get_int(self, section: str, key: str, default: int) -> int:
        """정수 값 읽기"""
        try:
            return self._config.getint(section, key)
        except (configparser.NoOptionError, ValueError):
            return default
    
    def _get_float(self, section: str, key: str, default: float) -> float:
        """실수 값 읽기"""
        try:
            return self._config.getfloat(section, key)
        except (configparser.NoOptionError, ValueError):
            return default
    
    def get_status(self) -> Dict:
        """현재 상태 반환"""
        return {
            "file_path": self._current_path,
            "file_exists": self._current_path and os.path.exists(self._current_path),
            "last_data": self._last_data.to_dict()
        }


# 전역 인스턴스
_gui_state_reader: Optional[GuiStateReader] = None


def get_gui_state_reader() -> GuiStateReader:
    """전역 GuiState 리더 가져오기"""
    global _gui_state_reader
    if _gui_state_reader is None:
        _gui_state_reader = GuiStateReader()
    return _gui_state_reader
