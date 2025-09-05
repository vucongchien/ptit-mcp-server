import requests
from typing import Dict, Any
from models import ScheduleResponse
from config import Config
import logging

logger = logging.getLogger(__name__)

SCHEDULE_URL = Config.schedule_url()


def get_schedule(access_token: str, cookies: Dict[str, str]) -> ScheduleResponse:
    """
    Lấy thời khóa biểu từ UIS PTIT.
    """
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "text/plain",
    }

    try:
        resp = requests.post(SCHEDULE_URL, headers=headers, cookies=cookies, timeout=10)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error("Error when fetching schedule: %s", e)
        return ScheduleResponse(status="fail", body=str(e))

    try:
        return ScheduleResponse(status="ok", data=resp.json())
    except ValueError as e:  # JSON decode error
        logger.error("Invalid JSON response: %s", e)
        return ScheduleResponse(status="fail", code=resp.status_code, body=resp.text)