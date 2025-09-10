# models.py
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, ConfigDict
from datetime import date, datetime

# -------------------
# Cấu trúc dữ liệu trả về khi login
class CurrUserData(BaseModel):
    IDUser: Optional[int]
    Session: Optional[int]
    id: Optional[int]
    name: Optional[str]
    FullName: Optional[str]
    principal: Optional[str]
    access_token: Optional[str]
    userName: Optional[str]
    roles: Optional[str]
    IDDVPC: Optional[int]
    UserLevel: Optional[int]
    result: Optional[bool]
    code: Optional[int]
    # Có thể thêm field khác nếu UIS trả về

    # Pydantic V2 config
    model_config = ConfigDict(
        extra="ignore",  # từ chối các field không khai báo
        populate_by_name=True  # cho phép alias mapping
    )


class LoginResponse(BaseModel):
    status: str
    redirect_url: Optional[str] = None
    curr_user: Optional[str] = None
    access_token: Optional[str] = None
    cookies: Optional[Dict[str, Any]] = None
    code: Optional[int] = None

    model_config = ConfigDict(extra="ignore")


# -------------------
# Cấu trúc từng tiết học trong ngày
class TietTrongNgay(BaseModel):
    tiet: int
    gio_bat_dau: Optional[str] = ""
    gio_ket_thuc: Optional[str] = ""
    so_phut: int
    nhhk: int

    model_config = ConfigDict(extra="ignore")


# -------------------
# Cấu trúc từng buổi học trong thời khóa biểu
class ThoiKhoaBieuEntry(BaseModel):
    is_hk_lien_truoc: int
    thu_kieu_so: int
    tiet_bat_dau: int
    so_tiet: int
    ma_mon: str
    ten_mon: str
    so_tin_chi: Optional[str] = None
    id_to_hoc: str
    id_tkb: str
    id_to_hop: str
    ma_nhom: str
    ma_to_th: Optional[str] = None
    ma_to_hop: Optional[str] = None
    ma_giang_vien: Optional[str] = None
    ten_giang_vien: Optional[str] = None
    ma_lop: Optional[str] = None
    ten_lop: Optional[str] = None
    ma_phong: Optional[str] = None
    ma_co_so: Optional[str] = None
    is_day_bu: bool
    ngay_hoc: str  # ISO format: "YYYY-MM-DDTHH:MM:SS"
    tiet_bat_dau_kttc: Optional[str] = None
    id_tu_tao: Optional[str] = None
    is_file_bai_giang: Optional[bool] = None
    id_sinh_hoat: Optional[str] = None
    is_dang_duyet_nghi_day: Optional[bool] = None
    is_nghi_day: Optional[bool] = None

    model_config = ConfigDict(extra="ignore")


# -------------------
# Cấu trúc từng tuần học
class TuanTKB(BaseModel):
    tuan_hoc_ky: int
    tuan_tuyet_doi: int
    thong_tin_tuan: str
    ngay_bat_dau: str  # ISO format
    ngay_ket_thuc: str  # ISO format
    ds_thoi_khoa_bieu: List[ThoiKhoaBieuEntry]

    model_config = ConfigDict(extra="ignore")


# -------------------
# Data chính trong response
class ScheduleData(BaseModel):
    total_items: int
    total_pages: int
    ds_tiet_trong_ngay: List[TietTrongNgay]
    ds_tuan_tkb: List[TuanTKB]

    model_config = ConfigDict(extra="ignore")


# -------------------
# Full API Response
class ScheduleFullResponse(BaseModel):
    status: str
    code: int
    data: Optional[ScheduleData] | str

    model_config = ConfigDict(extra="ignore")


# -------------------
# Cấu trúc thông báo
class Notification(BaseModel):
    id: str
    tieu_de: str
    noi_dung: Optional[str] = None
    ngay_gui: str  # ISO format
    nguoi_gui: str
    is_da_doc: bool

    model_config = ConfigDict(extra="ignore")


class NotificationResponse(BaseModel):
    total_items: int
    total_pages: int
    notification: int
    ds_thong_bao: List[Notification]

    model_config = ConfigDict(extra="ignore")
