import datetime
from typing import Dict, Optional,List,Tuple
from ptit_server.services.auth import login_ptit
from ptit_server.services.schedule import (
    get_schedule,
    get_schedule_for_day,
    get_schedule_for_week,
)
from ptit_server.services.notification import (
    get_all_notifications,
    get_unread_notifications
    
)
from ptit_server.utils.formatter import format_schedule_day, format_schedule_week
from ptit_server.models import ScheduleFullResponse, Notification




class PtitClient:
    def __init__(self, username: str, password: str,cache_ttl: int = 300):
        self.username = username
        self.password = password
        self.token: Optional[str] = None
        self.cookies: Optional[Dict[str, str]] = None
        self.full_schedule: Optional[ScheduleFullResponse] = None
        self._notifications_cache: Optional[Tuple[List[Notification], datetime.datetime]] = None
        self.cache_ttl = datetime.timedelta(seconds=cache_ttl)

    # ======================
    # AUTH
    # ======================
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
    
    # ======================
    # CACHE HELPER
    # ======================
    def _is_cache_valid(self, cache_obj: Optional[Tuple], ttl: datetime.timedelta) -> bool:
        if not cache_obj:
            return False
        _, ts = cache_obj
        return datetime.datetime.now() - ts < ttl
    
    
    # ======================
    # SCHEDULE
    # ======================
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
    
    # ======================
    # NOTIFICATIONS
    # ======================
    def fetch_notifications(self) -> list[Notification]:
        self.ensure_login()

        if self._is_cache_valid(self._notifications_cache, self.cache_ttl):
            return self._notifications_cache[0]

        resp = get_all_notifications(self.token,self.cookies)
        self._notifications_cache = (resp, datetime.datetime.now())
        return resp

    def fetch_unread_notifications(self) -> list[Notification]:
        self.ensure_login()
        # Không cache unread để đảm bảo real-time
        return get_unread_notifications(self.token,self.cookies)