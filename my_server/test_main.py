import datetime
from my_server.client.ptit_client import PtitClient

def test_fetch_schedule_today():
    username = "n22dccn109"
    password = "151124"
    client = PtitClient(username, password)
    result = client.fetch_schedule_today()
    print("Lịch hôm nay:")
    print(result)

def test_fetch_schedule_week():
    username = "n22dccn109"
    password = "151124"
    client = PtitClient(username, password)
    result = client.fetch_schedule_week()
    print("Lịch tuần:")
    print(result)

def test_fetch_schedule_for_day():
    username = "n22dccn109"
    password = "151124"
    client = PtitClient(username, password)
    date = datetime.date(2025, 8, 12)
    result = client.fetch_schedule_for_day(date)
    print(f"Lịch ngày {date.strftime('%d/%m/%Y')}:")
    print(result)

if __name__ == "__main__":
    test_fetch_schedule_today()
    test_fetch_schedule_week()
    test_fetch_schedule_for_day()
