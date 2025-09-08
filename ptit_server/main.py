# ptit_server/main.py
from fastmcp import FastMCP
from ptit_server.services.auth import login_ptit
from ptit_server.services.schedule import get_schedule, get_schedule_for_day, get_schedule_for_week
from ptit_server.utils.formatter import format_schedule_day, format_schedule_week
import datetime

mcp = FastMCP("Student Assistant Server 🎓")


@mcp.tool(tags=["public", "login"])
def login_and_get_token(username: str, password: str):
    """Đăng nhập UIS PTIT và trả về CurrUser token + cookies"""
    return login_ptit(username, password)   


@mcp.tool(tags=["public", "student"])
def fetch_schedule(access_token: str, cookies: dict):
    """Lấy thời khóa biểu từ UIS PTIT"""
    # Lấy TKB từ API
    resp = get_schedule(access_token, cookies)

    # Lịch hôm nay
    today = datetime.date.today()
    today_schedule = get_schedule_for_day(resp, today)
    print("=== Lịch hôm nay ===")
    print(format_schedule_day(today_schedule))

    # Lịch tuần này
    week_schedule = get_schedule_for_week(resp, today)
    print("\n=== Lịch tuần này ===")
    print(format_schedule_week(week_schedule))

    # Lịch cho 1 ngày bất kỳ
    custom_date = datetime.date(2025, 8, 12)
    custom_schedule = get_schedule_for_day(resp, custom_date)
    print("\n=== Lịch ngày 12/08/2025 ===")
    print(format_schedule_day(custom_schedule))

    return get_schedule(access_token, cookies)  


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=3000)
