from lib.Requests import Request
from lib.colors import *


async def bandlab4json(target: str):
    r = await Request("https://www.bandlab.com/api/v1.3/validation/user", params={'email': target}).get()
    data = r.json()

    if data.get('isValid'):
        if data.get('isAvailable') == False:
            return {"service": "Bandlab", "status": "found", "data": data}
        else:
            return {"service": "Bandlab", "status": "not found", "data": data}
    else:
        return {"service": "Bandlab", "status": "not found", "data": data}
