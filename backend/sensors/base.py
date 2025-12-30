"""
센서 베이스 클래스 (Template Method Pattern)
============================================

역할:
- ISensor: 모든 센서가 구현해야 하는 인터페이스
- BaseSensor: 공통 로직을 구현한 추상 클래스 (Template Method)

패턴:
- Template Method: connect(), get_data() 등의 공통 흐름 정의
- 서브클래스에서 _do_connect(), _do_get_data() 구현
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from collections import deque
import logging
import threading

logger = logging.getLogger("HBNU_Backend")


class ISensor(ABC):
    """센서 인터페이스 - 모든 센서가 구현해야 하는 메서드 정의"""
    
    @abstractmethod
    def connect(self) -> bool:
        """센서 연결"""
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """센서 연결 해제"""
        pass
    
    @abstractmethod
    def get_data(self) -> Optional[Dict[str, Any]]:
        """센서 데이터 수집"""
        pass
    
    @abstractmethod
    def is_connected(self) -> bool:
        """연결 상태 확인"""
        pass


class BaseSensor(ISensor):
    """
    센서 베이스 클래스 (Template Method Pattern)
    
    공통 로직:
    - 연결/해제 흐름
    - 에러 핸들링
    - 로깅
    
    서브클래스에서 구현:
    - _do_connect(): 실제 연결 로직
    - _do_disconnect(): 실제 연결 해제 로직
    - _do_get_data(): 실제 데이터 수집 로직
    """
    
    def __init__(self, config_path: Optional[str] = None, name: str = "Sensor"):
        """
        Args:
            config_path: 설정 파일 경로
            name: 센서 이름 (로깅용)
        """
        self._config_path = config_path
        self._name = name
        self._activate = False
        self._lock = threading.Lock()
    
    @property
    def name(self) -> str:
        return self._name
    
    def connect(self) -> bool:
        """
        Template Method: 센서 연결
        
        흐름:
        1. 연결 시도 로깅
        2. _do_connect() 호출 (서브클래스 구현)
        3. 결과 로깅 및 상태 업데이트
        """
        logger.info(f"[{self._name}] 연결 시도 중...")
        
        try:
            self._do_connect()
            self._activate = True
            logger.info(f"[{self._name}] 연결 성공")
            return True
        except Exception as e:
            self._activate = False
            logger.error(f"[{self._name}] 연결 실패: {e}")
            return False
    
    def disconnect(self) -> None:
        """
        Template Method: 센서 연결 해제
        """
        if not self._activate:
            return
        
        logger.info(f"[{self._name}] 연결 해제 중...")
        
        try:
            self._do_disconnect()
            self._activate = False
            logger.info(f"[{self._name}] 연결 해제 완료")
        except Exception as e:
            logger.error(f"[{self._name}] 연결 해제 실패: {e}")
    
    def get_data(self) -> Optional[Dict[str, Any]]:
        """
        Template Method: 데이터 수집
        
        흐름:
        1. 연결 상태 확인
        2. _do_get_data() 호출 (서브클래스 구현)
        3. 에러 핸들링
        """
        if not self._activate:
            return None
        
        try:
            with self._lock:
                return self._do_get_data()
        except Exception as e:
            logger.warning(f"[{self._name}] 데이터 수집 오류: {e}")
            return None
    
    def is_connected(self) -> bool:
        """연결 상태 반환"""
        return self._activate
    
    @abstractmethod
    def _do_connect(self) -> None:
        """
        서브클래스에서 구현할 실제 연결 로직
        
        예외 발생 시 connect()에서 처리됨
        """
        pass
    
    @abstractmethod
    def _do_disconnect(self) -> None:
        """
        서브클래스에서 구현할 실제 연결 해제 로직
        """
        pass
    
    @abstractmethod
    def _do_get_data(self) -> Dict[str, Any]:
        """
        서브클래스에서 구현할 실제 데이터 수집 로직
        
        Returns:
            Dict[str, Any]: 센서 데이터
        """
        pass


class SensorDataBuffer:
    """
    센서 데이터 버퍼 (공통 사용)
    
    역할:
    - 최근 데이터를 순환 버퍼에 저장
    - 스레드 안전한 데이터 접근
    """
    
    def __init__(self, max_size: int = 100):
        self._buffer = deque(maxlen=max_size)
        self._lock = threading.Lock()
        self._last_valid = None
    
    def store(self, data: Dict[str, Any]) -> None:
        """데이터 저장"""
        with self._lock:
            self._buffer.append(data)
            self._last_valid = data
    
    def retrieve(self) -> Optional[Dict[str, Any]]:
        """최신 데이터 조회"""
        with self._lock:
            if self._buffer:
                return self._buffer[-1]
            return self._last_valid
    
    def clear(self) -> None:
        """버퍼 초기화"""
        with self._lock:
            self._buffer.clear()
