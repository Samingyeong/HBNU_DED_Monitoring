"""
DED Trace 파일 감시 모듈
========================

역할:
- C:\DED\Log\Trace\ 폴더에서 가장 최근 파일 자동 감시
- 시작/종료 패턴 감지 → 자동저장 트리거
- WebSocket으로 프론트엔드에 실시간 알림

핵심 규칙:
- 날짜 기반이 아니라 가장 최근 수정된 파일 감시
- 백엔드에서만 파일 접근, 프론트엔드는 WebSocket으로 알림만 수신
"""
import os
import asyncio
import logging
from datetime import datetime
from typing import Optional, Callable, Dict, Any
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class TraceEvent:
    """Trace 이벤트 데이터"""
    event_type: str  # 'process_start', 'process_end', 'system_shutdown'
    timestamp: str
    message: str
    file_path: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class DEDTraceWatcher:
    """
    DED Trace 파일 감시자
    
    - 폴더 내 가장 최근 파일 자동 감지
    - 2초 간격으로 파일 변경 확인
    - 패턴 매칭으로 공정 시작/종료 감지
    """
    
    # 감시할 폴더 경로 (우선순위)
    TRACE_FOLDERS = [
        r'C:\DED\Log\Trace',
        r'D:\DED\Log\Trace',
    ]
    
    # 감지할 패턴
    PATTERNS = {
        'process_start': ['NC_CS5Axis,StartNormal', 'step,10'],  # 둘 다 포함해야 함
        'process_end': ['NC_CS5AXIS,IsRunning,False'],
        'system_shutdown': ['UnInit Completed'],
    }
    
    def __init__(self, check_interval: float = 2.0):
        self._check_interval = check_interval
        self._running = False
        self._task: Optional[asyncio.Task] = None
        
        # 현재 감시 중인 파일
        self._current_file: Optional[str] = None
        self._last_file_size: int = 0
        self._last_line_count: int = 0
        self._last_processed_line: str = ""
        
        # 콜백
        self._on_event_callbacks: list = []
        
        # 현재 상태
        self._is_process_running = False
        self._current_session_id: Optional[str] = None
        
        logger.info("🔍 DED Trace 감시자 초기화")
    
    def on_event(self, callback: Callable[[TraceEvent], None]):
        """이벤트 콜백 등록"""
        self._on_event_callbacks.append(callback)
    
    async def start(self):
        """감시 시작"""
        if self._running:
            logger.warning("⚠️ Trace 감시자가 이미 실행 중")
            return
        
        self._running = True
        self._task = asyncio.create_task(self._watch_loop())
        logger.info("🚀 DED Trace 파일 감시 시작")
    
    async def stop(self):
        """감시 중지"""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("🛑 DED Trace 파일 감시 중지")
    
    async def _watch_loop(self):
        """감시 루프"""
        while self._running:
            try:
                await self._check_trace_files()
            except Exception as e:
                logger.error(f"❌ Trace 파일 감시 오류: {e}")
            
            await asyncio.sleep(self._check_interval)
    
    async def _check_trace_files(self):
        """Trace 파일 확인"""
        # 가장 최근 파일 찾기
        latest_file = self._find_latest_trace_file()
        
        if not latest_file:
            return
        
        # 파일이 변경되었는지 확인
        try:
            file_size = os.path.getsize(latest_file)
        except OSError:
            return
        
        # 새 파일이거나 크기가 변경되었을 때만 처리
        if latest_file != self._current_file or file_size != self._last_file_size:
            self._current_file = latest_file
            self._last_file_size = file_size
            
            # 파일 내용 읽기
            await self._process_trace_file(latest_file)
    
    def _find_latest_trace_file(self) -> Optional[str]:
        """가장 최근 수정된 Trace 파일 찾기"""
        latest_file = None
        latest_mtime = 0
        
        for folder in self.TRACE_FOLDERS:
            if not os.path.exists(folder):
                continue
            
            try:
                for filename in os.listdir(folder):
                    if not filename.endswith('.txt'):
                        continue
                    
                    file_path = os.path.join(folder, filename)
                    try:
                        mtime = os.path.getmtime(file_path)
                        if mtime > latest_mtime:
                            latest_mtime = mtime
                            latest_file = file_path
                    except OSError:
                        continue
            except OSError:
                continue
        
        return latest_file
    
    async def _process_trace_file(self, file_path: str):
        """Trace 파일 처리"""
        try:
            # 파일 읽기 (다양한 인코딩 시도)
            content = None
            for encoding in ['utf-8', 'cp949', 'euc-kr', 'latin-1']:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if content is None:
                return
            
            # 줄 단위로 분리
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            
            if not lines:
                return
            
            # 새로운 줄만 처리 (마지막 몇 줄 확인)
            # 이전에 처리한 마지막 줄 이후의 새 줄들만 확인
            new_lines = []
            found_last = False
            
            if self._last_processed_line:
                for i, line in enumerate(lines):
                    if found_last:
                        new_lines.append(line)
                    elif line == self._last_processed_line:
                        found_last = True
                
                # 마지막 처리 줄을 못 찾았으면 (파일이 새로 생성됨) 전체 처리
                if not found_last:
                    new_lines = lines[-10:]  # 마지막 10줄만
            else:
                # 처음 시작이면 마지막 줄만 확인
                new_lines = lines[-1:]
            
            # 새 줄들에서 패턴 매칭
            for line in new_lines:
                await self._match_patterns(line, file_path, new_lines)
            
            # 마지막 처리 줄 업데이트
            if lines:
                self._last_processed_line = lines[-1]
                
        except Exception as e:
            logger.error(f"❌ Trace 파일 처리 오류: {e}")
    
    # 비상정지 관련 키워드 (Trace 로그에서 E-stop 추정용)
    _ESTOP_KEYWORDS = ('estop', 'e-stop', 'emergency', 'emg', '비상', 'esstop', 'emgstop')

    async def _match_patterns(self, line: str, file_path: str, context_lines: list = None):
        """패턴 매칭. context_lines: process_end 시 비상 키워드 검사용."""
        # 타임스탬프 추출 시도
        timestamp = ""
        if ',' in line:
            parts = line.split(',')
            if len(parts) >= 2:
                timestamp = f"{parts[0].strip()}, {parts[1].strip()}"
        
        # 공정 시작 패턴
        start_patterns = self.PATTERNS['process_start']
        if all(pattern in line for pattern in start_patterns):
            if not self._is_process_running:
                self._is_process_running = True
                self._current_session_id = datetime.now().strftime('%y%m%d_%H%M%S')
                
                event = TraceEvent(
                    event_type='process_start',
                    timestamp=timestamp or datetime.now().isoformat(),
                    message=line,
                    file_path=file_path,
                    metadata={'session_id': self._current_session_id}
                )
                
                logger.info(f"🚀 공정 시작 감지: {self._current_session_id}")
                await self._emit_event(event)
            return
        
        # 공정 종료 패턴
        for pattern in self.PATTERNS['process_end']:
            if pattern in line:
                if self._is_process_running:
                    self._is_process_running = False
                    # Trace 최근 줄에 비상정지 관련 키워드 있으면 estop 추정
                    haystack = (context_lines or [line])
                    estop_in_trace = any(
                        kw in (l or '').lower() for l in haystack for kw in self._ESTOP_KEYWORDS
                    )
                    meta = {'session_id': self._current_session_id, 'estop': bool(estop_in_trace)}
                    if estop_in_trace:
                        meta['estop_reason'] = 'Trace 파일 내 비상/긴급 관련 로그 감지'
                    event = TraceEvent(
                        event_type='process_end',
                        timestamp=timestamp or datetime.now().isoformat(),
                        message=line,
                        file_path=file_path,
                        metadata=meta
                    )
                    logger.info(f"🛑 공정 종료 감지: {self._current_session_id} (estop={estop_in_trace})")
                    self._current_session_id = None
                    await self._emit_event(event)
                return
        
        # 시스템 종료 패턴
        for pattern in self.PATTERNS['system_shutdown']:
            if pattern in line:
                if self._is_process_running:
                    self._is_process_running = False
                    haystack = (context_lines or [line])
                    estop_in_trace = any(
                        kw in (l or '').lower() for l in haystack for kw in self._ESTOP_KEYWORDS
                    )
                    meta = {'session_id': self._current_session_id, 'estop': bool(estop_in_trace)}
                    if estop_in_trace:
                        meta['estop_reason'] = 'Trace 파일 내 비상/긴급 관련 로그 감지'
                    event = TraceEvent(
                        event_type='system_shutdown',
                        timestamp=timestamp or datetime.now().isoformat(),
                        message=line,
                        file_path=file_path,
                        metadata=meta
                    )
                    logger.info(f"⚠️ 시스템 종료 감지 (estop={estop_in_trace})")
                    self._current_session_id = None
                    await self._emit_event(event)
                return
    
    async def _emit_event(self, event: TraceEvent):
        """이벤트 발생"""
        for callback in self._on_event_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(event)
                else:
                    callback(event)
            except Exception as e:
                logger.error(f"❌ 이벤트 콜백 오류: {e}")
    
    def get_status(self) -> Dict:
        """현재 상태 반환"""
        return {
            "is_watching": self._running,
            "current_file": self._current_file,
            "is_process_running": self._is_process_running,
            "current_session_id": self._current_session_id,
            "check_interval": self._check_interval
        }


# 전역 인스턴스
trace_watcher: Optional[DEDTraceWatcher] = None


def get_trace_watcher() -> DEDTraceWatcher:
    """전역 Trace 감시자 가져오기"""
    global trace_watcher
    if trace_watcher is None:
        trace_watcher = DEDTraceWatcher()
    return trace_watcher
