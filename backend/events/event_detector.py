"""
이벤트 감지기 (Event Detector)
================================

역할:
- 상태 전이(StateTransition)를 분석해서 의미 있는 이벤트로 변환
- Slack 알림 대상 이벤트 필터링

핵심 규칙:
- 모든 이벤트는 상태 전이에서만 발생
- 동일 이벤트 중복 방지 (쿨다운)
"""
import logging
from enum import Enum
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


class EventType(Enum):
    """이벤트 타입 정의"""
    # 공정 관련
    PROCESS_START = "process_start"       # 공정 시작
    PROCESS_END = "process_end"           # 공정 정상 종료
    PROCESS_ABORT = "process_abort"       # 공정 비정상 중단
    
    # 장비 상태
    EQUIPMENT_ERROR = "equipment_error"   # 장비 오류 발생
    EQUIPMENT_RECOVERED = "equipment_recovered"  # 장비 복구 완료
    
    # 연결 상태
    CONNECTION_LOST = "connection_lost"   # 연결 끊김
    CONNECTION_RESTORED = "connection_restored"  # 연결 복구
    
    # 시스템
    SYSTEM_STARTUP = "system_startup"     # 시스템 시작
    SYSTEM_SHUTDOWN = "system_shutdown"   # 시스템 종료


class EventLevel(Enum):
    """이벤트 심각도"""
    INFO = "info"           # 정보성 (파란색)
    WARNING = "warning"     # 경고 (노란색)
    CRITICAL = "critical"   # 치명적 (빨간색)


@dataclass
class Event:
    """이벤트 데이터 구조"""
    event_type: EventType
    level: EventLevel
    timestamp: datetime
    title: str
    message: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        return {
            "event_type": self.event_type.value,
            "level": self.level.value,
            "timestamp": self.timestamp.isoformat(),
            "title": self.title,
            "message": self.message,
            "metadata": self.metadata
        }


class EventDetector:
    """
    이벤트 감지기
    
    상태 전이를 분석해서 Slack 알림 대상 이벤트 생성
    """
    
    # 이벤트별 쿨다운 시간 (초)
    DEFAULT_COOLDOWN_SECONDS = 300  # 5분
    
    # 이벤트 타입별 레벨 매핑
    EVENT_LEVELS = {
        EventType.PROCESS_START: EventLevel.INFO,
        EventType.PROCESS_END: EventLevel.INFO,
        EventType.PROCESS_ABORT: EventLevel.WARNING,
        EventType.EQUIPMENT_ERROR: EventLevel.CRITICAL,
        EventType.EQUIPMENT_RECOVERED: EventLevel.INFO,
        EventType.CONNECTION_LOST: EventLevel.CRITICAL,
        EventType.CONNECTION_RESTORED: EventLevel.INFO,
        EventType.SYSTEM_STARTUP: EventLevel.INFO,
        EventType.SYSTEM_SHUTDOWN: EventLevel.INFO,
    }
    
    def __init__(self, cooldown_seconds: int = DEFAULT_COOLDOWN_SECONDS):
        self._cooldown_seconds = cooldown_seconds
        self._last_event_times: Dict[EventType, datetime] = {}
        self._event_history: list = []
        
        logger.info(f"🔍 이벤트 감지기 초기화 (쿨다운: {cooldown_seconds}초)")
    
    def detect_event(
        self,
        from_state: str,
        to_state: str,
        reason: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> Optional[Event]:
        """
        상태 전이를 분석해서 이벤트 감지
        
        Args:
            from_state: 이전 상태
            to_state: 새로운 상태
            reason: 전이 이유
            metadata: 추가 정보
        
        Returns:
            Event 객체 또는 None (이벤트 없음)
        """
        event_type = self._determine_event_type(from_state, to_state)
        
        if event_type is None:
            return None
        
        # 쿨다운 체크
        if self._is_on_cooldown(event_type):
            logger.debug(f"⏳ 이벤트 쿨다운 중: {event_type.value}")
            return None
        
        # 이벤트 생성
        event = self._create_event(event_type, from_state, to_state, reason, metadata)
        
        # 쿨다운 타이머 갱신
        self._last_event_times[event_type] = datetime.now()
        
        # 히스토리 저장
        self._event_history.append(event)
        if len(self._event_history) > 100:
            self._event_history = self._event_history[-100:]
        
        logger.info(f"🎯 이벤트 감지: {event_type.value} ({event.level.value})")
        
        return event
    
    def _determine_event_type(
        self, 
        from_state: str, 
        to_state: str
    ) -> Optional[EventType]:
        """상태 전이에서 이벤트 타입 결정"""
        
        # 공정 시작 (idle/starting → running)
        if from_state in ("idle", "starting") and to_state == "running":
            return EventType.PROCESS_START
        
        # 공정 정상 종료 (running → stopping → stopped)
        if from_state == "running" and to_state in ("stopping", "stopped"):
            return EventType.PROCESS_END
        
        if from_state == "stopping" and to_state == "stopped":
            return EventType.PROCESS_END
        
        # 공정 비정상 중단 (running → error)
        if from_state == "running" and to_state == "error":
            return EventType.PROCESS_ABORT
        
        # 장비 오류 (any → error)
        if to_state == "error" and from_state != "running":
            return EventType.EQUIPMENT_ERROR
        
        # 장비 복구 (error/recovering → idle)
        if from_state in ("error", "recovering") and to_state == "idle":
            return EventType.EQUIPMENT_RECOVERED
        
        # 연결 끊김 (any → disconnected)
        if to_state == "disconnected":
            return EventType.CONNECTION_LOST
        
        # 연결 복구 (disconnected → any)
        if from_state == "disconnected" and to_state != "error":
            return EventType.CONNECTION_RESTORED
        
        return None
    
    def _is_on_cooldown(self, event_type: EventType) -> bool:
        """이벤트가 쿨다운 중인지 확인"""
        last_time = self._last_event_times.get(event_type)
        
        if last_time is None:
            return False
        
        elapsed = (datetime.now() - last_time).total_seconds()
        return elapsed < self._cooldown_seconds
    
    def _create_event(
        self,
        event_type: EventType,
        from_state: str,
        to_state: str,
        reason: Optional[str],
        metadata: Optional[Dict]
    ) -> Event:
        """이벤트 객체 생성"""
        
        level = self.EVENT_LEVELS.get(event_type, EventLevel.INFO)
        title, message = self._get_event_message(event_type, from_state, to_state, reason)
        
        return Event(
            event_type=event_type,
            level=level,
            timestamp=datetime.now(),
            title=title,
            message=message,
            metadata={
                "from_state": from_state,
                "to_state": to_state,
                "reason": reason,
                **(metadata or {})
            }
        )
    
    def _get_event_message(
        self,
        event_type: EventType,
        from_state: str,
        to_state: str,
        reason: Optional[str]
    ) -> tuple:
        """이벤트 타입별 메시지 생성"""
        
        messages = {
            EventType.PROCESS_START: (
                "▶️ 공정 시작",
                "DED 공정이 시작되었습니다."
            ),
            EventType.PROCESS_END: (
                "✅ 공정 종료",
                "DED 공정이 정상적으로 완료되었습니다."
            ),
            EventType.PROCESS_ABORT: (
                "⚠️ 공정 중단",
                f"DED 공정이 비정상적으로 중단되었습니다.\n원인: {reason or '알 수 없음'}"
            ),
            EventType.EQUIPMENT_ERROR: (
                "🚨 장비 오류",
                f"장비에 오류가 발생했습니다.\n원인: {reason or '알 수 없음'}"
            ),
            EventType.EQUIPMENT_RECOVERED: (
                "🔧 장비 복구 완료",
                "장비가 정상 상태로 복구되었습니다."
            ),
            EventType.CONNECTION_LOST: (
                "🔌 연결 끊김",
                f"장비와의 연결이 끊어졌습니다.\n원인: {reason or '알 수 없음'}"
            ),
            EventType.CONNECTION_RESTORED: (
                "🔗 연결 복구",
                "장비와의 연결이 복구되었습니다."
            ),
            EventType.SYSTEM_STARTUP: (
                "🚀 시스템 시작",
                "DED 모니터링 시스템이 시작되었습니다."
            ),
            EventType.SYSTEM_SHUTDOWN: (
                "⏹️ 시스템 종료",
                "DED 모니터링 시스템이 종료되었습니다."
            ),
        }
        
        return messages.get(event_type, ("알림", "상태가 변경되었습니다."))
    
    def get_history(self, limit: int = 10) -> list:
        """최근 이벤트 이력"""
        return [e.to_dict() for e in self._event_history[-limit:]]
    
    def reset_cooldown(self, event_type: Optional[EventType] = None):
        """쿨다운 리셋"""
        if event_type:
            self._last_event_times.pop(event_type, None)
        else:
            self._last_event_times.clear()
        logger.info("🔄 이벤트 쿨다운 리셋")
