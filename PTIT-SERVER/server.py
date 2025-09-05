from fastmcp import FastMCP
from .services.auth import login_ptit
from .services.schedule import get_schedule

mcp = FastMCP("Student Assistant Server 🎓")


@mcp.tool(tags=["public", "login"])
def login_and_get_token(username: str, password: str):
    """Đăng nhập UIS PTIT và trả về CurrUser token + cookies"""
    return login_ptit(username, password)   


@mcp.tool(tags=["public", "student"])
def fetch_schedule(access_token: str, cookies: dict):
    """Lấy thời khóa biểu từ UIS PTIT"""
    return get_schedule(access_token, cookies)  


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=3000)
