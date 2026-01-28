# process_state_watcher.py
from slack_notifier import notify_start, notify_end, notify_estop
from datetime import datetime, timedelta

class ProcessStateWatcher:
    """
    running / estop boolean 입력을 받아
    '변화가 있을 때만' Slack 알림을 보냄.
    get_estop_status()로 상태머신/Trace에서 비상정지 여부 조회.
    """
    def __init__(self):
        self.prev_running = None
        self.prev_estop = None
        self._last_estop_reason = ""
        self._last_estop_notify_time = None  # 비상정지 알림 쿨다운용
        self._estop_cooldown_seconds = 300  # 5분 쿨다운

    def update(self, running: bool, estop: bool, estop_reason: str = ""):
        # 공정 시작: False -> True
        if self.prev_running is False and running is True:
            notify_start()

        # 공정 종료: True -> False (단, 비상정지면 종료 알림은 막음)
        if self.prev_running is True and running is False and not estop:
            notify_end()

        # 비상정지: False -> True (또는 None -> True) + 쿨다운 체크
        estop_just_activated = (self.prev_estop is False or self.prev_estop is None) and estop is True
        if estop_just_activated:
            now = datetime.now()
            # 쿨다운 체크: 마지막 알림 후 5분 이내면 스킵
            if self._last_estop_notify_time is None or (now - self._last_estop_notify_time).total_seconds() >= self._estop_cooldown_seconds:
                notify_estop(estop_reason)
                self._last_estop_notify_time = now

        # 상태 기억
        if estop:
            self._last_estop_reason = estop_reason or ""
        self.prev_running = running
        self.prev_estop = estop

    def get_estop_status(self):
        """(estop: bool, estop_reason: str) — Trace/상태머신에서 비상정지 메타 전달용."""
        return (self.prev_estop or False, getattr(self, "_last_estop_reason", "") or "")