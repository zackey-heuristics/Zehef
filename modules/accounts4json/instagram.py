"""

"""
from lib.Requests import Request
from lib.colors import *


async def instagram4json(target: str):
    req = await Request("https://www.instagram.com/accounts/emailsignup/").get()

    try:
        csrf_token = req.cookies.get('csrftoken')
        if not csrf_token:
            return {"service": "Instagram", "status": "error", "error": "CSRF token not found"}
    except Exception as e:
        return {"service": "Instagram", "status": "error", "error": f"CSRF token retrieval error: {str(e)}"}

    data = {
        'email': target,
        'first_name': '',
        'username': '',
        'opt_into_one_tap': False
    }

    r = await Request("https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/", 
                      headers={'x-csrftoken': csrf_token}, data=data).post()
    
    try:
        errors = r.json().get('errors', {})
        email_errors = errors.get('email', [])
        code = email_errors[0].get('code') if email_errors else None

        if code == 'email_is_taken':
            return {"service": "Instagram", "status": "found", "data": r.json()}
        else:
            return {"service": "Instagram", "status": "not found", "data": r.json()}

    except (KeyError, IndexError) as e:
        return {"service": "Instagram", "status": "error", "error": f"Response parsing error: {str(e)}"}
    except Exception as e:
        return {"service": "Instagram", "status": "error", "error": f"Unexpected error: {str(e)}"}
