import json
from datetime import datetime
from typing import List
import asyncio
import requests

from mailing.models import Mailing, Client, Message
from messenger.settings import API_URL, PROBE_TOKEN
import aiohttp


async def async_post_message(msg_id: int, msg: dict):
    url = f"{API_URL}/v1/send/{msg_id}"
    print(url)
    headers = {'Authorization': 'Bearer ' + PROBE_TOKEN}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=msg, headers=headers) as resp:
            response = await resp.json()
            return response.ok


def post_message(msg_id: int, msg: dict):
    url = f"{API_URL}/v1/send/{msg_id}"
    print(url)
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer ' + PROBE_TOKEN,
        'Content-Type': 'application/json'
    }
    response = requests.post(url, data=json.dumps(msg), headers=headers)
    print("for msg = ", msg)
    # print(response)
    # print(response.json())
    # print(response.__dict__)
    return response.ok

    # print('in do_mailing')
    # print(operator_id)
    # print(tag)


def do_mailing(mailing: Mailing):
    operator_id, tag = get_clients_filter(mailing)
    clients = pick_up_clients_for_mailing(operator_id, tag)
    execute_mailing(mailing, clients)


def get_clients_filter(mailing: Mailing) -> tuple[str, str]:
    operator_id, tag = mailing.mailing_filter.split('|')
    operator_id = operator_id.strip()
    tag = tag.strip()
    return operator_id, tag


def pick_up_clients_for_mailing(operator_id: str, tag: str) -> List[Client]:
    clients = Client.objects.filter(operator_id__iexact=operator_id).filter(tag__iexact=tag)
    print(clients)
    return clients


def execute_mailing(mailing: Mailing, clients: List[Client]):

    print(clients)

    for client in clients:
        current_time = datetime.now(mailing.terminate_at.tzinfo)

        print('mailing.terminate_at =', mailing.terminate_at, type(mailing.terminate_at))
        print('now = ', current_time, type(current_time))

        if mailing.terminate_at > current_time:

            print('Making a mailing')

            msg = create_message(mailing, client.pk)
            status_ok = post_message(msg.pk, {'id': msg.pk, 'phone': int(client.phone), 'text': mailing.text})
            msg.status = 'Success' if status_ok else 'Fail'
            msg.save()

            print(msg)


def create_message(mailing: Mailing, client_id: int) -> Message:
    msg = Message(mailing_id=mailing.pk, client_id=client_id, status='Awaited')
    msg.save()
    return msg
