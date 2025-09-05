import requests
import urllib.parse as urlparse
from typing import Dict
from ..utils.helper import encode_payload, parse_curr_user
from models import LoginResponse
from config import Config
import logging

logger = logging.getLogger(__name__)

BASE_URL = Config.login_url()


def build_code(username: str, password: str) -> str:
    """Tạo chuỗi code (Base64 JSON) cho API login"""
    payload = {
        "username": username,
        "password": password,
        "uri": "https://uis.ptithcm.edu.vn/#/home"
    }
    return encode_payload(payload)


def login_ptit(username: str, password: str) -> LoginResponse:
    code = build_code(username, password)
    url = f"{BASE_URL}?code={code}&gopage=&mgr=1"

    session = requests.Session()

    try:
        resp = session.get(url, allow_redirects=False, timeout=10)
    except requests.exceptions.RequestException as e:
        logger.error("Login request failed: %s", e)
        return LoginResponse(status="fail", code=None)

    if resp.status_code == 302:
        redirect_url = resp.headers.get("Location")
        if not redirect_url:
            logger.error("Redirect response without Location header")
            return LoginResponse(status="fail", code=302)

        logger.info("Redirect URL: %s", redirect_url)

        parsed = urlparse.urlparse(redirect_url)
        fragment_query = urlparse.parse_qs(urlparse.urlparse("?" + parsed.fragment).query)
        curr_user = fragment_query.get("/home?CurrUser", [None])[0]

        access_token = None
        if curr_user:
            try:
                access_token = parse_curr_user(curr_user).get("access_token")
            except Exception as e:
                logger.error("Failed to parse curr_user: %s", e)

        logger.debug("Access Token: %s", access_token)
        return LoginResponse(
            status="ok",
            redirect_url=redirect_url,
            curr_user=curr_user,
            access_token=access_token,
            cookies=session.cookies.get_dict()
        )

    logger.warning("Login failed with status %s", resp.status_code)
    return LoginResponse(status="fail", code=resp.status_code)