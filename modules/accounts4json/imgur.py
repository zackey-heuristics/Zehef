import requests
from lib.colors import *


def imgur4json(target: str):
    try:
        r = requests.post("https://imgur.com/signin/ajax_email_available", data={'email': target})
        json_data = r.json()
        available = json_data['data']['available']
        
        if available is True:
            return {"service": "Imgur", "status": "not found", "data": json_data}
        elif available is False:
            return {"service": "Imgur", "status": "found", "data": json_data}
        else:
            return {"service": "Imgur", "status": "error", "data": json_data}
    except Exception as e:
        return {"service": "Imgur", "status": "error", "error": str(e)}
