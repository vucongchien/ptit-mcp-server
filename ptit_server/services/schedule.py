#ptit_server/services/schdule.py
from typing import Dict, Optional, Any, List
import datetime
import requests
from ptit_server.models import ScheduleFullResponse, ScheduleData, TietTrongNgay, ThoiKhoaBieuEntry
from ptit_server.config import Config
import logging


# SCHEDULE_URL = Config.schedule_url()
HOCKY_URL="https://uis.ptithcm.edu.vn/api/sch/w-locdshockytkbuser"
#DOITUONGTHOIKHOABIEU_URL="https://uis.ptithcm.edu.vn/api/sch/w-locdsdoituongthoikhoabieu"
SCHEDULE_URL="https://uis.ptithcm.edu.vn/api/sch/w-locdstkbtuanusertheohocky"

logger = logging.getLogger(__name__)

def get_hocky(access_token: str, cookies: Dict[str, str]):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
    }
    
    resp_hocky = requests.post(
            HOCKY_URL,
            headers=headers,
            cookies=cookies,
            json={"filter": {"is_tieng_anh": None},
                  "additional": {"paging": {"limit": 100, "page": 1},
                                 "ordering": [{"name": "hoc_ky", "order_type": 1}]}}
    )
    
    if resp_hocky.status_code != 200:
        logger.error(f"Failed to get semester data: {resp_hocky.status_code}")
        return None
    
    try:
        hocky_data = resp_hocky.json()
        current_semester = hocky_data.get("data", {}).get("hoc_ky_theo_ngay_hien_tai")
        
        if current_semester:
            logger.info(f"Found current semester: {current_semester}")
            return current_semester
            
        # Fallback to first semester if current not found
        ds_hoc_ky = hocky_data.get("data", {}).get("ds_hoc_ky", [])
        if ds_hoc_ky:
            logger.warning("Current semester not found, using latest semester")
            return ds_hoc_ky[0]["hoc_ky"]
            
        logger.error("No semester data found")
        return ScheduleFullResponse(status="fail", code=404, data="Không tìm thấy học kỳ")
        
    except Exception as e:
        logger.error(f"Error parsing semester data: {e}")
        return None


def get_schedule(
    access_token: str,
    cookies: Dict[str, str],
    hoc_ky: Optional[int] = None,
    loai_doi_tuong: int = 1,
) -> ScheduleFullResponse:
    """
    Lấy thời khóa biểu từ UIS PTIT theo học kỳ và đối tượng.
    """

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
    }

    if hoc_ky is None:
        hoc_ky = get_hocky(access_token, cookies)
        if hoc_ky is None:
            return ScheduleFullResponse(
                status="fail", code=500, data="Không lấy được học kỳ hiện tại"
            )

    payload = {
        "filter": {"hoc_ky": hoc_ky, "loai_doi_tuong": loai_doi_tuong},
        "additional": {"paging": {"limit": 100, "page": 1}},
    }

    resp = requests.post(SCHEDULE_URL, headers=headers, cookies=cookies, json=payload)

    if resp.status_code == 200:
        try:
            parsed_data = ScheduleData(**resp.json()["data"])            
            return ScheduleFullResponse(status="ok", code=200, data=parsed_data)
        except Exception as e:
            logger.error(f"Parse schedule error: {e}")
            return ScheduleFullResponse(status="fail", code=500, data=str(e))

    return ScheduleFullResponse(status="fail", code=resp.status_code, data=resp.text)

def get_schedule_for_today(schedule: ScheduleFullResponse) -> List[ThoiKhoaBieuEntry]:
    """
    Lấy danh sách lịch học trong ngày hôm nay từ response TKB.
    """
    if not schedule or schedule.status != "ok":
        return []

    today = datetime.date.today()
    today_str = today.strftime("%Y-%m-%d")

    result: List[ThoiKhoaBieuEntry] = []
    ds_tuan = schedule.data.ds_tuan_tkb

    for tuan in ds_tuan:
        ds_tkb = tuan.ds_thoi_khoa_bieu
        for tkb in ds_tkb:
            ngay_hoc = tkb.ngay_hoc
            if ngay_hoc.startswith(today_str):
                result.append(tkb)

    return result


# =========================
# LẤY LỊCH THEO NGÀY/TUẦN
# =========================
def get_schedule_for_day(schedule: ScheduleFullResponse, date: datetime.date) -> List[ThoiKhoaBieuEntry]:
    """
    Lấy lịch cho 1 ngày bất kỳ.
    """
    if not schedule or schedule.status != "ok":
        return []

    date_str = date.strftime("%Y-%m-%d")
    result: List[ThoiKhoaBieuEntry] = []

    ds_tuan = schedule.data.ds_tuan_tkb

    for tuan in ds_tuan:
        for tkb in tuan.ds_thoi_khoa_bieu:
            ngay_hoc = tkb.ngay_hoc
            if ngay_hoc.startswith(date_str):
                result.append(tkb)
    return result


def get_schedule_for_week(schedule: ScheduleFullResponse, date: datetime.date) -> List[ThoiKhoaBieuEntry]:
    """
    Lấy lịch cho tuần chứa ngày bất kỳ.
    """
    if not schedule or schedule.status != "ok":
        return []

    result: List[ThoiKhoaBieuEntry] = []
    ds_tuan = schedule.data.ds_tuan_tkb

    for tuan in ds_tuan:
        try:
            # Use dot notation instead of dictionary access since tuan is a TuanTKB object
            ngay_bat_dau = datetime.datetime.strptime(tuan.ngay_bat_dau, "%d/%m/%Y").date()
            ngay_ket_thuc = datetime.datetime.strptime(tuan.ngay_ket_thuc, "%d/%m/%Y").date()

            if ngay_bat_dau <= date <= ngay_ket_thuc:
                result.extend(tuan.ds_thoi_khoa_bieu)
                
        except Exception as e:
            logger.error(f"Error processing week data: {e}")
            continue

    return result


