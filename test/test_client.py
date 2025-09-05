import asyncio
from fastmcp import Client
import json

client = Client("http://127.0.0.1:3000/mcp")

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