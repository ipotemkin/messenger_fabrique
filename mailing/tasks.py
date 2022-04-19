from typing import List

from celery import shared_task
from datetime import datetime

from mailing.models import Mailing, Client, Message
from mailing.probe_api import post_message


def do_mailing(mailing: Mailing) -> None:
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


def schedule_all_mailings():
    mailings = Mailing.objects.all()
    for mailing in mailings:
        launch_or_schedule_mailing(mailing)


def launch_or_schedule_mailing(mailing: Mailing):
    launch_at = mailing.launch_at
    terminate_at = mailing.terminate_at
    current_time = datetime.now(launch_at.tzinfo)

    if launch_at < current_time < terminate_at:
        do_mailing(mailing)
    elif current_time < launch_at and current_time < terminate_at:
        send_out_messages_for_mailing.apply_async((mailing.pk,), eta=launch_at)


def execute_mailing(mailing: Mailing, clients: List[Client]) -> None:

    print(clients)

    for client in clients:
        current_time = datetime.now(mailing.terminate_at.tzinfo)

        print('mailing.terminate_at =', mailing.terminate_at, type(mailing.terminate_at))
        print('now = ', current_time, type(current_time))

        if mailing.terminate_at > current_time:

            print('Making a mailing')

            msg = create_message(mailing, client.pk)
            status_ok = post_message(
                msg.pk,
                {
                    'id': msg.pk,
                    'phone': int(client.phone),
                    'text': mailing.text
                }
            )
            msg.status = 'Success' if status_ok else 'Fail'
            msg.save()

            print(msg)


def create_message(mailing: Mailing, client_id: int) -> Message:
    msg = Message(mailing_id=mailing.pk, client_id=client_id, status='Awaited')
    msg.save()
    return msg


@shared_task
def send_out_messages_for_mailing(mailing_id: int):
    mailing = Mailing.objects.get(pk=mailing_id)
    do_mailing(mailing)


@shared_task
def set_tasks_on_startup():
    print("Начальная установка тасков")
    schedule_all_mailings()
