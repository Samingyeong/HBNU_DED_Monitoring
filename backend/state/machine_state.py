"""
상태 머신 (State Machine) - DED 장비 상태 관리
============================================

상태 전이 다이어그램:
    IDLE → STARTING → RUNNING → STOPPING → STOPPED
                         ↓
                       ERROR
                         ↓
                    RECOVERING → IDLE

핵심 규칙:
- 같은 상태에 머무는 동안에는 이벤트 발생 X
- 상태 전이 시점에만 이벤트 발생
"""
import logging
from enum import Enum
from datetime import datetime
from typing import Optional, Callable, List
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


class MachineState(Enum):
    """장비 상태 정의"""
    IDLE = "idle"              # 대기 상태
    STARTING = "starting"      # 공정 시작 중
    RUNNING = "running"        # 공정 진행 중
    STOPPING = "stopping"      # 공정 종료 중
    STOPPED = "stopped"        # 공정 종료
    ERROR = "error"            # 오류 발생
    RECOVERING = "recovering"  # 복구 중
    DISCONNECTED = "disconnected"  # 연결 끊김


@dataclass
class StateTransition:
    """상태 전이 기록"""
    from_state: MachineState
    to_state: MachineState
    timestamp: datetime
    reason: Optional[str] = None
    metadata: dict = field(default_factory=dict)


class MachineStateManager:
    """
    장비 상태 관리자
    
    핵심 기능:
    1. 현재 상태 추적
    2. 상태 전이 감지
    3. 상태 변경 시 콜백 호출
    """
    
    # 허용된 상태 전이 정의
    VALID_TRANSITIONS = {
        MachineState.IDLE: [MachineState.STARTING, MachineState.DISCONNECTED],
        MachineState.STARTING: [MachineState.RUNNING, MachineState.ERROR, MachineState.IDLE],
        MachineState.RUNNING: [MachineState.STOPPING, MachineState.ERROR],
        MachineState.STOPPING: [MachineState.STOPPED, MachineState.ERROR],
        MachineState.STOPPED: [MachineState.IDLE],
        MachineState.ERROR: [MachineState.RECOVERING, MachineState.IDLE],
        MachineState.RECOVERING: [MachineState.IDLE, MachineState.ERROR],
        MachineState.DISCONNECTED: [MachineState.IDLE, MachineState.ERROR],
    }
    
    def __init__(self, initial_state: MachineState = MachineState.IDLE):
        self._current_state = initial_state
        self._previous_state: Optional[MachineState] = None
        self._state_entered_at = datetime.now()
        self._transition_history: List[StateTransition] = []
        self._on_transition_callbacks: List[Callable[[StateTransition], None]] = []
        
        logger.info(f"🔧 상태 머신 초기화: {initial_state.value}")
    
    @property
    def current_state(self) -> MachineState:
        """현재 상태 반환"""
        return self._current_state
    
    @property
    def previous_state(self) -> Optional[MachineState]:
        """이전 상태 반환"""
        return self._previous_state
    
    @property
    def state_duration_seconds(self) -> float:
        """현재 상태 유지 시간 (초)"""
        return (datetime.now() - self._state_entered_at).total_seconds()
    
    def can_transition_to(self, new_state: MachineState) -> bool:
        """특정 상태로 전이 가능한지 확인"""
        valid_targets = self.VALID_TRANSITIONS.get(self._current_state, [])
        return new_state in valid_targets
    
    def transition_to(
        self, 
        new_state: MachineState, 
        reason: Optional[str] = None,
        metadata: Optional[dict] = None,
        force: bool = False
    ) -> Optional[StateTransition]:
        """
        상태 전이 수행
        
        Args:
            new_state: 새로운 상태
            reason: 전이 이유
            metadata: 추가 메타데이터
            force: 유효성 검사 무시 (비상시에만 사용)
        
        Returns:
            StateTransition 객체 (전이 성공 시) 또는 None
        """
        # 같은 상태면 무시 (이벤트 발생 X)
        if new_state == self._current_state:
            return None
        
        # 유효한 전이인지 확인
        if not force and not self.can_transition_to(new_state):
            logger.warning(
                f"⚠️ 유효하지 않은 상태 전이: {self._current_state.value} → {new_state.value}"
            )
            return None
        
        # 상태 전이 기록 생성
        transition = StateTransition(
            from_state=self._current_state,
            to_state=new_state,
            timestamp=datetime.now(),
            reason=reason,
            metadata=metadata or {}
        )
        
        # 상태 업데이트
        self._previous_state = self._current_state
        self._current_state = new_state
        self._state_entered_at = datetime.now()
        self._transition_history.append(transition)
        
        # 히스토리 크기 제한 (최근 100개만 유지)
        if len(self._transition_history) > 100:
            self._transition_history = self._transition_history[-100:]
        
        logger.info(
            f"🔄 상태 전이: {transition.from_state.value} → {transition.to_state.value}"
            f" (사유: {reason or 'N/A'})"
        )
        
        # 콜백 호출
        for callback in self._on_transition_callbacks:
            try:
                callback(transition)
            except Exception as e:
                logger.error(f"❌ 상태 전이 콜백 오류: {e}")
        
        return transition
    
    def on_transition(self, callback: Callable[[StateTransition], None]):
        """상태 전이 콜백 등록"""
        self._on_transition_callbacks.append(callback)
        logger.debug(f"📌 상태 전이 콜백 등록됨 (총 {len(self._on_transition_callbacks)}개)")
    
    def get_history(self, limit: int = 10) -> List[StateTransition]:
        """최근 상태 전이 이력 반환"""
        return self._transition_history[-limit:]
    
    def to_dict(self) -> dict:
        """현재 상태를 딕셔너리로 반환"""
        return {
            "current_state": self._current_state.value,
            "previous_state": self._previous_state.value if self._previous_state else None,
            "state_entered_at": self._state_entered_at.isoformat(),
            "state_duration_seconds": round(self.state_duration_seconds, 2),
            "transition_count": len(self._transition_history)
        }


# ============================================
# 센서 데이터 기반 상태 판단 헬퍼
# ============================================

def determine_state_from_sensor_data(
    cnc_connected: bool,
    cnc_running: bool,
    laser_power: float,
    has_error: bool
) -> MachineState:
    """
    센서 데이터를 기반으로 장비 상태 판단
    
    이 함수는 상태를 "결정"만 하고, 실제 전이는 MachineStateManager에서 수행
    """
    if not cnc_connected:
        return MachineState.DISCONNECTED
    
    if has_error:
        return MachineState.ERROR
    
    if cnc_running and laser_power > 0:
        return MachineState.RUNNING
    
    if cnc_running and laser_power == 0:
        return MachineState.STARTING
    
    return MachineState.IDLE
