"""
Slack 알림 모듈 (Slack Notifier)
================================

역할:
- Event를 받아서 Slack Webhook으로 전송
- 알림 메시지 포맷팅
- 전송 실패 시 재시도

핵심 규칙:
- Webhook URL은 환경변수에서 로드
- 센서/UI에서 직접 호출 금지 → Event만 처리
"""
import os
import logging
import asyncio
import aiohttp
from datetime import datetime
from typing import Optional, Dict, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class SlackConfig:
    """Slack 설정"""
    webhook_url: str
    enabled: bool = True
    channel: str = "#ded-monitoring"
    equipment_id: str = "DED-01"
    equipment_name: str = "HBNU DED Monitoring"
    max_retries: int = 3
    retry_delay: float = 1.0


class SlackNotifier:
    """
    Slack 알림 전송기
    
    사용법:
        notifier = SlackNotifier.from_env()
        await notifier.send_event(event)
    """
    
    # 이벤트 레벨별 이모지/색상
    LEVEL_COLORS = {
        "info": "#36a64f",      # 초록
        "warning": "#ff9800",   # 주황
        "critical": "#dc3545",  # 빨강
    }
    
    LEVEL_EMOJIS = {
        "info": "ℹ️",
        "warning": "⚠️",
        "critical": "🚨",
    }
    
    def __init__(self, config: SlackConfig):
        self._config = config
        self._session: Optional[aiohttp.ClientSession] = None
        self._send_count = 0
        self._error_count = 0
        
        if config.enabled:
            logger.info(f"📢 Slack 알림 활성화 (채널: {config.channel})")
        else:
            logger.info("📢 Slack 알림 비활성화됨")
    
    @classmethod
    def from_env(cls) -> "SlackNotifier":
        """환경변수에서 설정 로드"""
        from dotenv import load_dotenv
        load_dotenv()
        
        webhook_url = os.getenv("SLACK_WEBHOOK_URL", "")
        enabled = os.getenv("SLACK_ENABLED", "true").lower() == "true"
        channel = os.getenv("SLACK_CHANNEL", "#ded-monitoring")
        equipment_id = os.getenv("EQUIPMENT_ID", "DED-01")
        equipment_name = os.getenv("EQUIPMENT_NAME", "HBNU DED Monitoring")
        
        if not webhook_url and enabled:
            logger.warning("⚠️ SLACK_WEBHOOK_URL이 설정되지 않음 - Slack 알림 비활성화")
            enabled = False
        
        config = SlackConfig(
            webhook_url=webhook_url,
            enabled=enabled,
            channel=channel,
            equipment_id=equipment_id,
            equipment_name=equipment_name,
        )
        
        return cls(config)
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """HTTP 세션 가져오기 (재사용)"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=10)
            )
        return self._session
    
    async def close(self):
        """리소스 정리"""
        if self._session and not self._session.closed:
            await self._session.close()
            logger.debug("🔒 Slack HTTP 세션 종료")
    
    async def send_event(self, event: Any) -> bool:
        """
        이벤트를 Slack으로 전송
        
        Args:
            event: Event 객체 (event_detector.py에서 생성)
        
        Returns:
            전송 성공 여부
        """
        if not self._config.enabled:
            logger.debug("📢 Slack 비활성화 - 전송 건너뜀")
            return False
        
        try:
            # 이벤트에서 필요한 정보 추출
            event_dict = event.to_dict() if hasattr(event, 'to_dict') else event
            
            payload = self._build_payload(event_dict)
            success = await self._send_webhook(payload)
            
            if success:
                self._send_count += 1
                logger.info(f"✅ Slack 알림 전송 성공 (총 {self._send_count}회)")
            
            return success
            
        except Exception as e:
            self._error_count += 1
            logger.error(f"❌ Slack 알림 전송 실패: {e}")
            return False
    
    def _build_payload(self, event: Dict[str, Any]) -> Dict:
        """Slack 메시지 페이로드 생성"""
        
        level = event.get("level", "info")
        color = self.LEVEL_COLORS.get(level, "#808080")
        emoji = self.LEVEL_EMOJIS.get(level, "📢")
        
        title = event.get("title", "알림")
        message = event.get("message", "")
        timestamp = event.get("timestamp", datetime.now().isoformat())
        metadata = event.get("metadata", {})
        
        # 시간 포맷팅
        if isinstance(timestamp, str):
            try:
                dt = datetime.fromisoformat(timestamp)
                formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                formatted_time = timestamp
        else:
            formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        
        # Slack Block Kit 형식
        payload = {
            "attachments": [
                {
                    "color": color,
                    "blocks": [
                        {
                            "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": f"{emoji} {title}",
                                "emoji": True
                            }
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": message
                            }
                        },
                        {
                            "type": "context",
                            "elements": [
                                {
                                    "type": "mrkdwn",
                                    "text": f"*장비:* {self._config.equipment_id} | *시간:* {formatted_time}"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        
        # 메타데이터가 있으면 추가
        if metadata and metadata.get("from_state") and metadata.get("to_state"):
            payload["attachments"][0]["blocks"].insert(2, {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*이전 상태:*\n{metadata['from_state']}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*현재 상태:*\n{metadata['to_state']}"
                    }
                ]
            })
        
        return payload
    
    async def _send_webhook(self, payload: Dict) -> bool:
        """Webhook으로 메시지 전송 (재시도 포함)"""
        
        session = await self._get_session()
        
        for attempt in range(self._config.max_retries):
            try:
                async with session.post(
                    self._config.webhook_url,
                    json=payload
                ) as response:
                    if response.status == 200:
                        return True
                    else:
                        text = await response.text()
                        logger.warning(
                            f"⚠️ Slack 응답 오류 (시도 {attempt + 1}/{self._config.max_retries}): "
                            f"{response.status} - {text}"
                        )
            
            except asyncio.TimeoutError:
                logger.warning(f"⏱️ Slack 타임아웃 (시도 {attempt + 1}/{self._config.max_retries})")
            
            except Exception as e:
                logger.warning(f"⚠️ Slack 전송 오류 (시도 {attempt + 1}/{self._config.max_retries}): {e}")
            
            # 재시도 전 대기
            if attempt < self._config.max_retries - 1:
                await asyncio.sleep(self._config.retry_delay)
        
        return False
    
    async def send_test_message(self) -> bool:
        """테스트 메시지 전송"""
        test_event = {
            "event_type": "test",
            "level": "info",
            "timestamp": datetime.now().isoformat(),
            "title": "🧪 테스트 알림",
            "message": "Slack 연동이 정상적으로 작동합니다!",
            "metadata": {}
        }
        
        return await self.send_event(test_event)
    
    def get_stats(self) -> Dict:
        """전송 통계"""
        return {
            "enabled": self._config.enabled,
            "send_count": self._send_count,
            "error_count": self._error_count,
            "equipment_id": self._config.equipment_id,
        }


# ============================================
# 동기 래퍼 (기존 코드 호환용)
# ============================================

_notifier_instance: Optional[SlackNotifier] = None


def get_slack_notifier() -> SlackNotifier:
    """전역 Slack 알림 인스턴스 가져오기"""
    global _notifier_instance
    if _notifier_instance is None:
        _notifier_instance = SlackNotifier.from_env()
    return _notifier_instance


def send_slack_notification_sync(event: Any) -> bool:
    """동기 방식으로 Slack 알림 전송"""
    notifier = get_slack_notifier()
    
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # 이벤트 루프가 이미 실행 중이면 태스크 생성
            future = asyncio.ensure_future(notifier.send_event(event))
            return True  # 비동기로 전송됨
        else:
            return loop.run_until_complete(notifier.send_event(event))
    except RuntimeError:
        # 이벤트 루프가 없으면 새로 생성
        return asyncio.run(notifier.send_event(event))
