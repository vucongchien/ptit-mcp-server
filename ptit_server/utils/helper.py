
import base64
import json
from typing import Dict
import urllib.parse as urlparse
from typing import Optional
from ptit_server.models import CurrUserData

def encode_payload(payload: Dict) -> str:
    """Encode dict -> Base64 JSON string"""
    raw = json.dumps(payload, ensure_ascii=False)
    return base64.b64encode(raw.encode()).decode()

def decode_payload(code: str) -> Dict:
    """Decode Base64 JSON string -> dict"""
    raw = base64.b64decode(code).decode()
    return json.loads(raw)

def parse_curr_user(curr_user: str) -> Optional[CurrUserData]:
    """
    Giải mã CurrUser từ URL fragment:
    1. URL decode
    2. Base64 decode
    3. Parse JSON -> CurrUserData model
    """
    if not curr_user:
        return None
    try:
        decoded_url = urlparse.unquote(curr_user)
        data = decode_payload(decoded_url)
        print("DEBUG CurrUser decoded:", data) 
        return CurrUserData(**data)
    except Exception as e:
        print("Error decode CurrUser:", e)
        return None
