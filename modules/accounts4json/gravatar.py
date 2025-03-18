from lib.Requests import Request
from lib.colors import *
import hashlib


async def gravatar4json(target: str):
    encoded_email = target.lower().encode('utf-8')
    hashed_email = hashlib.sha256(encoded_email).hexdigest()

    try:
        r = await Request(f"https://en.gravatar.com/{hashed_email}.json").get()

        if "User not found" in r.text:
            return {"service": "Gravatar", "status": "not found", "data": None}
        else:
            data = r.json().get('entry', [{}])[0]
            result = {
                "service": "Gravatar",
                "status": "found",
                "username": data.get("displayName"),
                "account": f"https://gravatar.com/{data.get('displayName')}/",
            }

            try:
                avatar_url_seaked = data.get('thumbnailUrl', '')
                avatar_url = str(avatar_url_seaked).replace("\\", "")
                result["avatar"] = avatar_url
            except Exception:
                result["avatar"] = None

            return result

    except Exception as e:
        return {"service": "Gravatar", "status": "error", "error": str(e)}
