from lib.Requests import Request
from lib.colors import *


async def strava4json(target: str):
    params = {'email': target}
    try:
        req = await Request("https://www.strava.com/frontend/athletes/email_unique", params=params).get()
        if "false" in req.text:
            return {"service": "Strava", "status": "found", "data": req.text}
        elif "true" in req.text:
            return {"service": "Strava", "status": "not found", "data": req.text}
        else:
            return {"service": "Strava", "status": "error", "data": req.text}
    except Exception as e:
        return {"service": "Strava", "status": "error", "error": str(e)}
