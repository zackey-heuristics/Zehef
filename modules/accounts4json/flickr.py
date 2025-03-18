from lib.Requests import Request
from lib.colors import *
import re


async def flickr4json(target: str):
    result = {"service": "Flickr", "status": None, "data": None}
    count = 0

    try:
        r = await Request("https://www.flickr.com/").get()
    except Exception as e:
        return {"service": "Flickr", "status": "error", "error": str(e)}

    key_pattern = r'[a-f0-9]{32}'
    keys = re.findall(key_pattern, r.text)
    api_keys = set(keys)

    if api_keys:
        for key in api_keys:
            api = "https://api.flickr.com/services/rest"
            params = {
                'username': target,
                'exact': 0,
                'extras': 'path_alias%2Crev_ignored%2Crev_contacts%2Cis_pro%2Cicon_urls%2Clocation%2Crev_contact_count%2Cuse_vespa%2Cdate_joined',
                'per_page': 5,
                'page': 0,
                'show_more': 1,
                'perPage': 50,
                'loadFullContact': 1,
                'viewerNSID': None,
                'method': 'flickr.people.search',
                'api_key': key,
                'format': 'json',
                'hermes': 1,
                'hermesClient': 1,
                'nojsoncallback': 1
            }
            try:
                r2 = await Request(api, params=params).get()
                data = r2.json()['people']['person'][0]
                account_url = f"https://www.flickr.com/people/{data['nsid']}/"
                result = {
                    "service": "Flickr",
                    "status": "found",
                    "username": data.get("username"),
                    "name": data.get("realname") if data.get("realname") != '' else None,
                    "dbid": data.get("dbid"),
                    "account": account_url,
                    "data": data
                }
                count += 1
                break
            except Exception:
                continue

    if count == 0:
        result = {"service": "Flickr", "status": "not found", "data": None}

    return result
