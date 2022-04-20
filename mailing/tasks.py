from typing import List

from celery import shared_task
from datetime import datetime

from django.db.models import Q

from mailing.models import Mailing, Client, Message
from mailing.probe_api import post_message


def do_mailing(mailing: Mailing) -> None:
    """Осуществляет рассылку"""

    clients = get_clients_by_filter(mailing.mailing_filter)
    execute_mailing(mailing, clients)


def get_clients_by_filter(mailing_filter: str) -> List[Client]:
    """Возвращает список клиентов согласно фильтру в рассылке"""

    filter_lst = mailing_filter.strip().split('|')
    filter_len = len(filter_lst)

    query = Q()

    # if no filter
    if filter_len < 1:
        return query

    query_operator = Q()
    query_tag = Q()

    # if any tag in the filter
    if filter_len > 1 and (tags_str := filter_lst[1]):
        tags = [tag.strip() for tag in tags_str.split(',')]
        for tag in tags:
            query_tag |= Q(tag__iexact=tag)

    # if any operator_id in the filter
    if operator_ids_str := filter_lst[0]:
        operator_ids = [operator_id.strip() for operator_id in operator_ids_str.split(',')]
        for operator_id in operator_ids:
            query_operator |= Q(operator_id__iexact=operator_id)

    query = query_operator & query_tag
    clients = Client.objects.filter(query)
    return clients


def schedule_all_mailings() -> None:
    """Поставить в расписание все рассылки в базе"""

    mailings = Mailing.objects.all()
    for mailing in mailings:
        launch_or_schedule_mailing(mailing)


def launch_or_schedule_mailing(mailing: Mailing) -> None:
    """Запустить рассылку или поставить ее в расписание. Работает только в отношении актуальных рассылок"""

    launch_at = mailing.launch_at
    terminate_at = mailing.terminate_at
    current_time = datetime.now(launch_at.tzinfo)

    if launch_at < current_time < terminate_at:
        do_mailing(mailing)
    elif current_time < launch_at and current_time < terminate_at:
        send_out_messages_for_mailing.apply_async((mailing.pk,), eta=launch_at)


def execute_mailing(mailing: Mailing, clients: List[Client]) -> None:
    """Выполняет рассылку сообщений переданным в аргументах клиентам"""

    for client in clients:
        current_time = datetime.now(mailing.terminate_at.tzinfo)
        if mailing.terminate_at > current_time:
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


def create_message(mailing: Mailing, client_id: int) -> Message:
    """Создает сообщение в базе данных"""

    msg = Message(mailing_id=mailing.pk, client_id=client_id, status='Awaited')
    msg.save()
    return msg


@shared_task
def send_out_messages_for_mailing(mailing_id: int) -> None:
    """Запускает конкретную рассылку согласно установленному расписанию"""

    mailing = Mailing.objects.get(pk=mailing_id)
    do_mailing(mailing)


@shared_task
def set_tasks_on_startup() -> None:
    """Устанавливает расписание рассылок при старте/рестарте приложения """

    schedule_all_mailings()
