
from fastmcp import FastMCP
from my_server.client.ptit_client import PtitClient
import datetime

mcp = FastMCP("uis-mcp")


# Tool lấy lịch hôm nay
@mcp.tool(tags=["public", "student", "today"])
def fetch_schedule_today(username: str, password: str):
    """Lấy thời khóa biểu hôm nay từ UIS PTIT"""
    client = PtitClient(username, password)
    today_schedule = client.fetch_schedule_today()
    print("=== Lịch hôm nay ===")
    print(today_schedule)
    return today_schedule

# Tool lấy lịch tuần
@mcp.tool(tags=["public", "student", "week"])
def fetch_schedule_week(username: str, password: str, date: str = None):
    """Lấy thời khóa biểu tuần từ UIS PTIT. Nếu không truyền ngày, lấy tuần hiện tại."""
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

# Tool lấy lịch ngày bất kỳ
@mcp.tool(tags=["public", "student", "day"])
def fetch_schedule_for_day(username: str, password: str, date: str):
    """Lấy thời khóa biểu cho một ngày bất kỳ từ UIS PTIT"""
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
