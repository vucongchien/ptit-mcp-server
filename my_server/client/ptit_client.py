import datetime
from typing import Dict, Optional
from my_server.services.auth import login_ptit
from my_server.services.schedule import (
    get_schedule,
    get_schedule_for_day,
    get_schedule_for_week,
)
from my_server.utils.formatter import format_schedule_day, format_schedule_week
from my_server.models import ScheduleFullResponse




class PtitClient:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.token: Optional[str] = None
        self.cookies: Optional[Dict[str, str]] = None
        self.full_schedule: ScheduleFullResponse = None

    def login(self) -> bool:
        """Login UIS PTIT và lưu session"""
        try:
            result = login_ptit(self.username, self.password)
            self.token = result.access_token
            self.cookies = result.cookies
            return True
        except Exception as e:
            print(f"Login failed: {e}")
            return False

    def is_logged_in(self) -> bool:
        return self.token is not None and self.cookies is not None

    def ensure_login(self)->None:
        if not self.is_logged_in():
            success = self.login()
            if not success:
                raise RuntimeError("Không thể login, vui lòng kiểm tra tài khoản")
    
    def fetch_schedule(self):
        """Lấy full thời khóa biểu"""
        if self.full_schedule is not None:
            return self.full_schedule
        self.ensure_login()
        self.full_schedule = get_schedule(self.token, self.cookies)
        return self.full_schedule

    def fetch_schedule_today(self) -> str:
        self.ensure_login()
        resp = self.fetch_schedule()
        today = datetime.date.today()
        today_schedule = get_schedule_for_day(resp, today)
        return format_schedule_day(today_schedule)

    def fetch_schedule_week(self, date: Optional[datetime.date] = None) -> str:
        self.ensure_login()
        resp = self.fetch_schedule()
        if date is None:
            date = datetime.date.today()
        week_schedule = get_schedule_for_week(resp, date)
        return format_schedule_week(week_schedule)

    def fetch_schedule_for_day(self, date: datetime.date) -> str:
        self.ensure_login()
        resp = self.fetch_schedule()
        custom_schedule = get_schedule_for_day(resp, date)
        return format_schedule_day(custom_schedule)
