from lib.Requests import Request
from lib.colors import *


async def pinterest4json(target: str):
    params = {
        "source_url": "/",
        "data": '{"options": {"email": "' + target + '"}, "context": {}}'
    }

    try:
        r = await Request("https://www.pinterest.fr/resource/EmailExistsResource/get/", params=params).get()
        json_data = r.json()
        resource_data = json_data.get("resource_response", {}).get("data")
        if resource_data:
            return {"service": "Pinterest", "status": "found", "data": json_data}
        else:
            return {"service": "Pinterest", "status": "not found", "data": json_data}
    except Exception as e:
        return {"service": "Pinterest", "status": "error", "error": str(e)}
