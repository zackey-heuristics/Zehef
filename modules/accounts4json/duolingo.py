from lib.Requests import Request
from lib.colors import *


async def duolingo4json(target: str):
    r = await Request("https://www.duolingo.com/2017-06-30/users", params={'email': target}).get()

    try:
        json_data = r.json()
        users = json_data.get("users", [])
        if not users:
            return {"service": "Duolingo", "status": "not found", "data": json_data}
        else:
            username = users[0].get("username", "")
            return {"service": "Duolingo", "status": "found", "username": username, "data": json_data}
    except Exception as e:
        return {"service": "Duolingo", "status": "error", "error": str(e)}
