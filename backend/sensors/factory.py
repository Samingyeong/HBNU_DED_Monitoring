"""
센서 팩토리 (Factory Pattern)
=============================

역할:
- 센서 객체 생성을 중앙화
- 센서 타입별 클래스 등록/관리
- SensorManager와 센서 구현체 간의 결합도 감소

사용법:
    # 센서 등록 (모듈 로드 시 자동)
    SensorFactory.register('camera', CameraSensor)
    
    # 센서 생성
    sensor = SensorFactory.create('camera', config_path='...')
"""
from typing import Dict, Type, Optional, List
import logging

from .base import ISensor

logger = logging.getLogger("HBNU_Backend")


class SensorFactory:
    """
    센서 팩토리 (Factory Pattern)
    
    클래스 메서드로 구현하여 전역적으로 사용 가능
    """
    
    _sensors: Dict[str, Type[ISensor]] = {}
    _configs: Dict[str, str] = {}
    
    @classmethod
    def register(cls, sensor_type: str, sensor_class: Type[ISensor], 
                 default_config: Optional[str] = None) -> None:
        """
        센서 클래스 등록
        
        Args:
            sensor_type: 센서 타입 식별자 (예: 'camera', 'laser')
            sensor_class: ISensor를 구현한 센서 클래스
            default_config: 기본 설정 파일 경로
        """
        if not issubclass(sensor_class, ISensor):
            raise TypeError(f"{sensor_class.__name__}는 ISensor를 구현해야 합니다")
        
        cls._sensors[sensor_type] = sensor_class
        if default_config:
            cls._configs[sensor_type] = default_config
        
        logger.debug(f"센서 등록됨: {sensor_type} -> {sensor_class.__name__}")
    
    @classmethod
    def unregister(cls, sensor_type: str) -> None:
        """센서 클래스 등록 해제"""
        if sensor_type in cls._sensors:
            del cls._sensors[sensor_type]
        if sensor_type in cls._configs:
            del cls._configs[sensor_type]
    
    @classmethod
    def create(cls, sensor_type: str, **kwargs) -> ISensor:
        """
        센서 객체 생성
        
        Args:
            sensor_type: 센서 타입 식별자
            **kwargs: 센서 생성자에 전달할 인자
            
        Returns:
            ISensor: 생성된 센서 인스턴스
            
        Raises:
            ValueError: 등록되지 않은 센서 타입
        """
        if sensor_type not in cls._sensors:
            available = ', '.join(cls._sensors.keys()) or '없음'
            raise ValueError(
                f"알 수 없는 센서 타입: '{sensor_type}'. "
                f"등록된 센서: [{available}]"
            )
        
        # 기본 설정 파일 적용 (kwargs에 없는 경우)
        if 'config_path' not in kwargs and sensor_type in cls._configs:
            kwargs['config_path'] = cls._configs[sensor_type]
        
        sensor_class = cls._sensors[sensor_type]
        logger.info(f"센서 생성: {sensor_type} ({sensor_class.__name__})")
        
        return sensor_class(**kwargs)
    
    @classmethod
    def create_safe(cls, sensor_type: str, **kwargs) -> Optional[ISensor]:
        """
        안전한 센서 객체 생성 (예외 시 None 반환)
        
        Args:
            sensor_type: 센서 타입 식별자
            **kwargs: 센서 생성자에 전달할 인자
            
        Returns:
            Optional[ISensor]: 생성된 센서 인스턴스 또는 None
        """
        try:
            return cls.create(sensor_type, **kwargs)
        except Exception as e:
            logger.warning(f"센서 생성 실패 ({sensor_type}): {e}")
            return None
    
    @classmethod
    def get_registered_types(cls) -> List[str]:
        """등록된 센서 타입 목록 반환"""
        return list(cls._sensors.keys())
    
    @classmethod
    def is_registered(cls, sensor_type: str) -> bool:
        """센서 타입 등록 여부 확인"""
        return sensor_type in cls._sensors
    
    @classmethod
    def clear(cls) -> None:
        """모든 등록 센서 초기화 (테스트용)"""
        cls._sensors.clear()
        cls._configs.clear()


def register_sensor(sensor_type: str, default_config: Optional[str] = None):
    """
    센서 클래스 등록 데코레이터
    
    사용법:
        @register_sensor('camera')
        class CameraSensor(BaseSensor):
            ...
    """
    def decorator(cls: Type[ISensor]) -> Type[ISensor]:
        SensorFactory.register(sensor_type, cls, default_config)
        return cls
    return decorator
