from lib.colors import *
from lib.Requests import Request

async def x4json(target: str):
    try:
        r = await Request(f"https://api.twitter.com/i/users/email_available.json?email={target}").get()
        data = r.json()
        if data.get('taken'):
            return {"service": "X", "status": "found", "data": data}
        else:
            return {"service": "X", "status": "not found", "data": data}
    except Exception as e:
        return {"service": "X", "status": "error", "error": str(e)}
