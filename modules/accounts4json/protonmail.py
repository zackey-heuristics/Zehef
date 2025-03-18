"""
LICENSE => MIT License
This module comes from => https://github.com/Kr0wZ/NeutrOSINT

Github : https://github.com/Kr0wZ
𝕏 : https://x.com/ZworKrowZ
"""

from lib.Requests import Request
from lib.colors import *
from datetime import datetime
import json
import re 

Session = Request(url=None).Session()


async def generate_auth_cookie():
    url_session = "https://account.proton.me/api/auth/v4/sessions"
    url_cookies = "https://account.proton.me/api/core/v4/auth/cookies"

    data_session = {
        "x-pm-appversion": "web-account@5.0.153.3",
        "x-pm-locale": "en_US",
        "x-enforce-unauthsession": "true"
    }

    response = Session.post(url_session, headers=data_session)

    json_dump = json.loads(response.text)
    access_token = json_dump['AccessToken']
    refresh_token = json_dump['RefreshToken']
    uid = json_dump['UID']

    data_cookie = {
        "x-pm-appversion": "web-account@5.0.153.3",
        "x-pm-locale": "en_US",
        "x-pm-uid": uid,
        "Authorization": f"Bearer {access_token}"
    }

    request_data = {
        "GrantType": "refresh_token",
        "Persistent": 0,
        "RedirectURI": "https://protonmail.com",
        "RefreshToken": refresh_token,
        "ResponseType": "token",
        "State": "C72g4sTNltu4TAL5bUQlnvUT",
        "UID": uid
    }

    response = Session.post(url_cookies, headers=data_cookie, json=request_data)

    auth_cookie = None
    for cookie in response.cookies:
        if "AUTH" in str(cookie):
            auth_cookie = str(cookie).split(" ")[1]
            break

    return uid, auth_cookie


async def protonmail4json(target: str):
    valid_domains = ['pm.me', 'proton.me', 'protonmail.com', 'protonmail.ch']
    
    if target.split('@')[1] not in valid_domains:
        Session.close()
        return {"service": "Protonmail", "status": "error", "error": "Invalid Protonmail domain."}

    try:
        uid, auth_cookie = await generate_auth_cookie()

        headers = {
            "x-pm-appversion": "web-account@5.0.153.3",
            "x-pm-locale": "en_US",
            "x-pm-uid": uid,
            "Cookie": auth_cookie
        }

        params = {
            "Name": target,
            "ParseDomain": "1"
        }

        r = Session.get("https://account.proton.me/api/core/v4/users/available", headers=headers, params=params)

        if '"Suggestions":[]' in r.text or '"Code":1000' in r.text:
            result = {"service": "Protonmail", "status": "not found", "data": r.text}
        else:
            result = {"service": "Protonmail", "status": "found", "data": r.text}

            api = f"https://api.protonmail.ch/pks/lookup?op=index&search={target}"
            r_lookup = await Request(api).get()
            match = re.search(r'\b\d{10}\b', r_lookup.text)
            if match:
                timestamp = int(match.group())
                date_of_creation = datetime.fromtimestamp(timestamp)
                result["created_on"] = date_of_creation.strftime("%Y-%m-%d %H:%M:%S")
        return result

    except Exception as e:
        return {"service": "Protonmail", "status": "error", "error": str(e)}

    finally:
        Session.close()