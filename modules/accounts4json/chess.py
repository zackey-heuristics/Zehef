from lib.Requests import Request
from lib.colors import *


async def chess4json(target: str):
    r = await Request(f"https://www.chess.com/callback/email/available?email={target}").post()

    try:
        json_data = r.json()
        is_available = json_data.get('isEmailAvailable')
        if is_available is True:
            return {"service": "Chess", "status": "not found", "data": json_data}
        elif is_available is False:
            return {"service": "Chess", "status": "found", "data": json_data}
        else:
            return {"service": "Chess", "status": "error", "data": json_data}
    except Exception as e:
        return {"service": "Chess", "status": "error", "error": str(e)}
