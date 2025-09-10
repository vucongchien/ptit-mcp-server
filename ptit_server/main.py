
from fastmcp import FastMCP
from ptit_server.client.ptit_client import PtitClient
import datetime

mcp = FastMCP("ptithcm-mcp")

# ======================
# Notifications Tools
# ======================

@mcp.tool(tags=["public", "student", "notifications", "all"])
def fetch_notifications(username: str, password: str):
    """Lấy tất cả thông báo từ UIS PTIT (có cache)"""
    client = PtitClient(username, password)
    notifications = client.fetch_notifications()
    print("=== Tất cả thông báo ===")
    for n in notifications:
        print(f"[{n.date}] {n.title} - {n.content}")
    return notifications


@mcp.tool(tags=["public", "student", "notifications", "unread"])
def fetch_unread_notifications(username: str, password: str):
    """Lấy thông báo chưa đọc từ UIS PTIT (real-time)"""
    client = PtitClient(username, password)
    unread_notifications = client.fetch_unread_notifications()
    print("=== Thông báo chưa đọc ===")
    for n in unread_notifications:
        print(f"[{n.date}] {n.title} - {n.content}")
    return unread_notifications


# ======================
# Schedule Tools 
# ======================

@mcp.tool(tags=["public", "student", "today"])
def fetch_schedule_today(username: str, password: str):
    client = PtitClient(username, password)
    today_schedule = client.fetch_schedule_today()
    print("=== Lịch hôm nay ===")
    print(today_schedule)
    return today_schedule

@mcp.tool(tags=["public", "student", "week"])
def fetch_schedule_week(username: str, password: str, date: str = None):
    client = PtitClient(username, password)
    if date:
        try:
            date_obj = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        except Exception:
            date_obj = datetime.date.today()
    else:
        date_obj = datetime.date.today()
    week_schedule = client.fetch_schedule_week(date_obj)
    print("=== Lịch tuần ===")
    print(week_schedule)
    return week_schedule

@mcp.tool(tags=["public", "student", "day"])
def fetch_schedule_for_day(username: str, password: str, date: str):
    client = PtitClient(username, password)
    try:
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    except Exception:
        date_obj = datetime.date.today()
    custom_schedule = client.fetch_schedule_for_day(date_obj)
    print(f"=== Lịch ngày {date_obj.strftime('%d/%m/%Y')} ===")
    print(custom_schedule)
    return custom_schedule


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=3000)
