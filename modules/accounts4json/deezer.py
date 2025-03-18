from lib.Requests import Request
from lib.colors import *


def deezer4json(target: str):
    s = Request(url=None).Session()
    try:
        r = s.post("https://www.deezer.com/ajax/gw-light.php?method=deezer.getUserData&input=3&api_version=1.0&api_token=&cid=")
        token = r.json()['results']['checkForm']

        params = {
            'method': 'deezer.emailCheck',
            'input': 3,
            'api_version': 1.0,
            'api_token': token,
        }

        api = s.post("https://www.deezer.com/ajax/gw-light.php", params=params, data='{"EMAIL":"' + target + '"}')
        availability = api.json()['results']['availability']

        if availability is True:
            return {"service": "Deezer", "status": "not found", "data": api.json()}
        elif availability is False:
            return {"service": "Deezer", "status": "found", "data": api.json()}
        else:
            return {"service": "Deezer", "status": "error", "data": api.json()}
    except Exception as e:
        return {"service": "Deezer", "status": "error", "error": str(e)}
    finally:
        s.close()
