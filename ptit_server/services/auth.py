#ptit_server/services/auth.py
import requests
import urllib.parse as urlparse
from typing import Dict

from ptit_server.utils.helper import encode_payload, parse_curr_user
from ptit_server.models import LoginResponse
from ptit_server.config import Config

BASE_URL = Config.login_url()


def build_code(username: str, password: str) -> str:
    """
    Tạo chuỗi code (Base64 JSON) cho API login.
    """
    payload = {
        "username": username,
        "password": password,
        "uri": "https://uis.ptithcm.edu.vn/#/home"
    }
    return encode_payload(payload)


def login_ptit(username: str, password: str) -> LoginResponse:
    """
    Đăng nhập vào UIS PTIT.

    Args:
        username (str): Tài khoản sinh viên.
        password (str): Mật khẩu sinh viên.

    Returns:
        LoginResponse: Kết quả đăng nhập với thông tin:
            {
                "status": "ok/fail",
                "redirect_url": "...",
                "curr_user": "...",
                "access_token": "...",
                "cookies": {...}
            }
    """
    code = build_code(username, password)
    url = f"{BASE_URL}?code={code}&gopage=&mgr=1"

    session = requests.Session()
    resp = session.get(url, allow_redirects=False)

    if resp.status_code == 302:
        redirect_url = resp.headers["Location"]

        parsed = urlparse.urlparse(redirect_url)
        fragment_query = urlparse.parse_qs(
            urlparse.urlparse("?" + parsed.fragment).query
        )

        curr_user = fragment_query.get("/home?CurrUser", [None])[0]
        
        access_token = parse_curr_user(curr_user).access_token if curr_user else None


        print("Access Token:", access_token)

        
        return LoginResponse(
            status="ok",
            redirect_url=redirect_url,
            curr_user=curr_user,
            access_token=access_token,
            cookies=session.cookies.get_dict()
        )

    return LoginResponse(
        status="fail",
        code=resp.status_code
    )
