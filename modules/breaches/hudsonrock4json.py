from lib.Requests import Request
from lib.colors import *
import json
from datetime import datetime

from .hudsonrock import Cavalier

class Cavalier4JSON(Cavalier):
    async def loader(self):
        response = await Request(
            self.api,
            headers={'api-key': 'ROCKHUDSONROCK'},
            params={'email': self.email}
        ).get()

        result = {}
        try:
            stealers_data = response.json().get('stealers', [])

            if stealers_data:
                data = stealers_data[0]

                result['result'] = "compromised"
                result['total_corporate_services'] = data.get('total_corporate_services', '/')
                result['total_user_services'] = data.get('total_user_services', '/')

                time_iso = data.get('date_compromised')
                t_datetime = datetime.fromisoformat(time_iso.replace("Z", "+00:00"))
                result['date_compromised'] = t_datetime.strftime("%Y-%m-%d %H:%M:%S")

                result['computer_name'] = data.get('computer_name', '/')
                result['operating_system'] = data.get('operating_system', '/')
                result['ip_address'] = data.get('ip', '/')

                result['top_passwords'] = data.get('top_passwords', [])
                result['top_logins'] = data.get('top_logins', [])
            else:
                result['result'] = "safe"

            return result

        except (KeyError, json.JSONDecodeError) as e:
            return {
                'error': "Decode error",
                'exception': str(e)
            }
