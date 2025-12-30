"""
센서 모듈 패키지
================

GoF 디자인 패턴 적용:
- Factory Pattern: 센서 객체 생성
- Template Method Pattern: 공통 센서 로직
- Strategy Pattern: 센서별 통신 전략 (Socket, Serial, DLL)

사용법:
    from sensors import SensorFactory
    
    # 센서 생성
    camera = SensorFactory.create('camera')
    laser = SensorFactory.create('laser')
    
    # 연결
    camera.connect()
    
    # 데이터 수집
    data = camera.get_data()
    
    # 연결 해제
    camera.disconnect()
"""
from .base import ISensor, BaseSensor, SensorDataBuffer
from .factory import SensorFactory, register_sensor

# 센서 클래스 임포트 (Factory에 자동 등록됨)
from .camera import CameraSensor
from .laser import LaserSensor
from .pyrometer import PyrometerSensor
from .cnc import CnCSensor

__all__ = [
    # 인터페이스 및 베이스
    'ISensor', 
    'BaseSensor', 
    'SensorDataBuffer',
    
    # 팩토리
    'SensorFactory', 
    'register_sensor',
    
    # 센서 클래스
    'CameraSensor',
    'LaserSensor',
    'PyrometerSensor',
    'CnCSensor',
]
