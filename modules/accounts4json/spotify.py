from lib.Requests import Request
from lib.colors import *


async def spotify4json(target: str):
    try:
        r = await Request(f"https://spclient.wg.spotify.com/signup/public/v1/account?validate=1&email={target}").get()
        json_data = r.json()
        if json_data.get('status') == 20:
            return {"service": "Spotify", "status": "found", "data": json_data}
        else:
            return {"service": "Spotify", "status": "not found", "data": json_data}
    except Exception as e:
        return {"service": "Spotify", "status": "error", "error": str(e)}
