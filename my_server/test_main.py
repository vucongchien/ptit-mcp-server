import datetime
from my_server.client.ptit_client import PtitClient

# ======================
# Schedule Tests
# ======================

def test_fetch_schedule_today():
    username = "n22dccn109"
    password = "151124"
    client = PtitClient(username, password)
    result = client.fetch_schedule_today()
    print("=== Lịch hôm nay ===")
    print(result)

def test_fetch_schedule_week():
    username = "n22dccn109"
    password = "151124"
    client = PtitClient(username, password)
    result = client.fetch_schedule_week()
    print("=== Lịch tuần ===")
    print(result)

def test_fetch_schedule_for_day():
    username = "n22dccn109"
    password = "151124"
    client = PtitClient(username, password)
    date = datetime.date(2025, 8, 12)
    result = client.fetch_schedule_for_day(date)
    print(f"=== Lịch ngày {date.strftime('%d/%m/%Y')} ===")
    print(result)


# ======================
# Notifications Tests
# ======================

def test_fetch_notifications():
    username = "n22dccn109"
    password = "151124"
    client = PtitClient(username, password)
    notifications = client.fetch_notifications()
    print("=== Tất cả thông báo ===")
    for n in notifications:
        print(f"[{n.id}] {n.tieu_de} ")

def test_fetch_unread_notifications():
    username = "n22dccn109"
    password = "151124"
    client = PtitClient(username, password)
    unread_notifications = client.fetch_unread_notifications()
    print("=== Thông báo chưa đọc ===")
    for n in unread_notifications:
        print(f"[{n.date}] {n.title} - {n.content}")


# ======================
# Run all tests
# ======================

if __name__ == "__main__":
    # Schedule
    test_fetch_schedule_today()
    test_fetch_schedule_week()
    test_fetch_schedule_for_day()

    # Notifications
    test_fetch_notifications()
    test_fetch_unread_notifications()
