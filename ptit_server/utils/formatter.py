from typing import List
from ptit_server.models import ThoiKhoaBieuEntry

def format_schedule_day(list_tkb: List[ThoiKhoaBieuEntry]) -> str:
    """
    Format lịch cho 1 ngày ra string dễ đọc.
    """
    if not list_tkb:
        return "Không có lịch học."

    formatted = []
    for tkb in list_tkb:
        thu =  f"Thứ {tkb.thu_kieu_so}"
        time_range = f"Tiết {tkb.tiet_bat_dau} - {tkb.tiet_bat_dau + tkb.so_tiet - 1}"
        formatted.append(
            f"{thu} - {tkb.ten_mon} ({time_range}, phòng {tkb.ma_phong})"
        )

    return "\n".join(formatted)


def format_schedule_week(list_tkb: List[ThoiKhoaBieuEntry]) -> str:
    """
    Format lịch cho nguyên tuần.
    """
    if not list_tkb:
        return "Không có lịch học trong tuần."

    # sort theo thứ, tiết
    list_tkb.sort(key=lambda x: (x.thu_kieu_so, x.tiet_bat_dau))

    return "\n".join([format_schedule_day([tkb]) for tkb in list_tkb])