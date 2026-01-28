import json
import os
import requests
from datetime import datetime

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "").strip()  # 환경변수 권장

def _send_slack(text: str):
    if not SLACK_WEBHOOK_URL:
        print("[Slack] SLACK_WEBHOOK_URL이 설정되지 않았습니다.")
        return

    payload = {"text": text}
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json; charset=utf-8"}

    try:
        r = requests.post(SLACK_WEBHOOK_URL, data=data, headers=headers, timeout=5)
        r.raise_for_status()
    except Exception as e:
        print(f"[Slack] send fail: {e}")

def notify_start(extra: str = ""):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _send_slack(f"🚀 *DED 공정 시작*\n- 시각: {now}" + (f"\n- {extra}" if extra else ""))

def notify_end(extra: str = ""):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _send_slack(f"🛑 *DED 공정 종료*\n- 시각: {now}" + (f"\n- {extra}" if extra else ""))

def notify_estop(reason: str = ""):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _send_slack(f"🧯 *비상정지(E-STOP) 감지*\n- 시각: {now}" + (f"\n- 사유: {reason}" if reason else ""))