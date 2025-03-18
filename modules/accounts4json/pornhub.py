from bs4 import BeautifulSoup
from lib.Requests import Request
from lib.colors import *


def pornhub4json(target: str):
    s = Request(url=None).Session()
    try:
        r = s.get("https://fr.pornhub.com/signup")
        soup = BeautifulSoup(r.text, 'html.parser')
        token = soup.find(attrs={'name': 'token'}).get('value')

        params = {'token': token}
        data = {
            'check_what': 'email', 
            'email': target
        }

        api = s.post("https://fr.pornhub.com/user/create_account_check", params=params, data=data)
        result = api.json().get('email', None)

        if result == "create_account_passed":
            return {"service": "Pornhub", "status": "not found", "data": api.json()}

        elif result == "create_account_failed":
            return {"service": "Pornhub", "status": "found", "data": api.json()}
        else:
            return {"service": "Pornhub", "status": "error", "data": api.json()}
    except Exception as e:
        return {"service": "Pornhub", "status": "error", "error": str(e)}
    finally:
        s.close()
