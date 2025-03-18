from lib.colors import *
from lib.Requests import *


async def adobe4json(target: str):
    data = {
        "username": target,
        "usernameType": "EMAIL"
    }

    headers = {
        'x-ims-clientid': 'homepage_milo',
        'content-type': 'application/json'
    }

    r = await Request("https://auth.services.adobe.com/signin/v2/users/accounts", headers=headers, json=data).post()

    try:
        json_data = r.json()
        if json_data[0].get('authenticationMethods'):
            return {"service": "Adobe", "status": "found", "data": json_data}
        else:
            return {"service": "Adobe", "status": "not found", "data": json_data}

    except Exception as e:
        return {"service": "Adobe", "status": "error", "error": str(e)}