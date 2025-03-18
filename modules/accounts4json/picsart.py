from lib.Requests import Request
from lib.colors import *


async def picsart4json(target: str):
    params = {
        'email_encoded': 1,
        'emails': target
    }
    
    try:
        r = await Request("https://api.picsart.com/users/email/existence", params=params).get()
        json_data = r.json()
    except Exception as e:
        return {"service": "Picsart", "status": "error", "error": str(e)}

    if json_data.get('status') == 'success':
        if json_data.get('response'):
            return {"service": "Picsart", "status": "found", "data": json_data}
        else:
            return {"service": "Picsart", "status": "not found", "data": json_data}
    else:
        return {"service": "Picsart", "status": "error", "error": "Ratelimit", "data": json_data}
