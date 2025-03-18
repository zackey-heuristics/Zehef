from lib.Requests import Request
from lib.colors import *
from datetime import datetime


async def github4json(target: str):
    try:
        r = await Request(f"https://api.github.com/search/users?q={target}+in:email").get()
        search_json = r.json()

        if search_json.get("total_count", 0) == 0:
            return {"service": "Github", "status": "not found", "data": None}

        data = search_json.get("items", [])[0]

        api = await Request(f"https://api.github.com/users/{data['login']}").get()
        user_json = api.json()

        creation = user_json.get('created_at')
        update = user_json.get('updated_at')
        c_date = None
        u_date = None

        if creation:
            c_datetime = datetime.fromisoformat(creation.replace("Z", "+00:00"))
            c_date = c_datetime.strftime("%Y-%m-%d %H:%M:%S")
        if update:
            u_datetime = datetime.fromisoformat(update.replace("Z", "+00:00"))
            u_date = u_datetime.strftime("%Y-%m-%d %H:%M:%S")

        result = {
            "service": "Github",
            "status": "found",
            "username": data.get("login"),
            "name": user_json.get("name"),
            "id": data.get("id"),
            "avatar": data.get("avatar_url"),
            "created_on": c_date,
            "updated_on": u_date,
            "account_url": f"https://github.com/{data.get('login')}/",
            "data": data
        }
        return result

    except Exception as e:
        return {"service": "Github", "status": "error", "error": str(e)}
