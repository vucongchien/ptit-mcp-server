import requests
from typing import List, Dict
from ptit_server.models import NotificationResponse, Notification
from ptit_server.config import Config

BASE_URL = Config.notification_url()

def fetch_notifications(token: str, cookies: Dict[str, str]) -> List[Notification]:
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
    }

    payload = {
        "filter": {"id": None, "is_noi_dung": True, "is_web": True},
        "additional": {
            "paging": {"limit": 9999, "page": 1},
            "ordering": [{"name": "ngay_gui", "order_type": 1}],
        },
    }

    resp = requests.post(BASE_URL, headers=headers, cookies=cookies, json=payload)
    resp.raise_for_status()

    data = resp.json().get("data", {})
    parsed = NotificationResponse(**data)
    return parsed.ds_thong_bao


def get_unread_notifications(token: str, cookies: Dict[str, str]) -> List[Notification]:
    all_notifications = fetch_notifications(token, cookies)
    return [n for n in all_notifications if not n.is_da_doc]


def get_all_notifications(token: str, cookies: Dict[str, str]) -> List[Notification]:
    return fetch_notifications(token, cookies)
