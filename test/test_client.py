import asyncio
from fastmcp import Client
import json
from typing import Dict, Any
from pydantic import BaseModel

client = Client("http://127.0.0.1:3000/mcp")

class scheduleResponse(BaseModel):
    status: str
    data: Any = None
    code: int = None
    body: str = None

class PTITClient(Client):
    def __init__(self, server_url: str = "http://127.0.0.1:3000/mcp"):
        self.client = Client(server_url)
        self.access_token = None
        self.cokies = None
        
    async def login(self, username: str, password: str):
        login_result = await client.call_tool("login_and_get_token", {
            "username": username,
            "password": password
        })
        
        login_data = json.loads(login_result.content[0].text)
        self.access_token = login_data["access_token"]
        self.cookies = login_data["cookies"]
        
        #chua co xu ly loi 
    
    async def get_schedule(self) -> Dict[str, Any]:
        if not self.access_token or not self.cookies:
            raise ValueError("Chua login")
        
        schedule_result = await client.call_tool("fetch_schedule", {
            "access_token": self.access_token,
            "cookies": self.cookies
        })
        
        print("Schedule:", schedule_result.content[0].text)

        
    

async def main():
    async with client:
        # gọi login
        login_result = await client.call_tool("login_and_get_token", {
            "username": "n22dccn109",
            "password": "151124"
        })
        # Lấy text JSON và parse thành dict
        login_data = json.loads(login_result.content[0].text)
        print("Login result:", login_data)
        print("✅ Login success")

        # Dùng dict để truyền cho tool tiếp theo
        schedule_result = await client.call_tool("fetch_schedule", {
            "access_token": login_data["access_token"],
            "cookies": login_data["cookies"]
        })
        print("Schedule:", schedule_result.content[0].text)

if __name__ == "__main__":
    asyncio.run(main())