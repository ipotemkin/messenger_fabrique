import json
import requests

from messenger.settings import API_URL, PROBE_TOKEN


def post_message(msg_id: int, msg: dict) -> bool:
    url = f"{API_URL}/v1/send/{msg_id}"
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer ' + PROBE_TOKEN,
        'Content-Type': 'application/json'
    }
    response = requests.post(url, data=json.dumps(msg), headers=headers)
    return response.ok
