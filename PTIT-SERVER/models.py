from typing import Optional, Dict, Any
from pydantic import BaseModel

class CurrUserData(BaseModel):
    IDUser: Optional[int]
    Session: Optional[int]
    id: Optional[int]
    name: Optional[str]
    FullName: Optional[str]
    principal: Optional[str]
    access_token: Optional[str]
    username: Optional[str]
    roles: Optional[str]
    IDDVPC: Optional[int]
    UserLevel: Optional[int]
    result: Optional[str]
    code: Optional[int]
    # có thể thêm field khác nếu UIS trả về

class LoginResponse(BaseModel):
    status: str
    redirect_url: Optional[str] = None
    curr_user: Optional[str] = None
    access_token: Optional[str] = None
    cookies: Optional[Dict] = None
    code: Optional[int] = None

class ScheduleResponse(BaseModel):
    status: str
    data: Optional[Any] = None
    code: Optional[int] = None
    body: Optional[str] = None