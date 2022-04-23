from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets, permissions
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from mailing.models import Client, Mailing, Message
from mailing.serializers import (
    ClientSerializer,
    MailingSerializer,
    MsgSerializer,
    MsgRetrieveSerializer,
    MailingListSerializer,
    MailingRetrieveSerializer
)
from mailing.tasks import launch_or_schedule_mailing


@extend_schema_view(
    list=extend_schema(description="Получить список клиентов", summary="Список клиентов"),
    retrieve=extend_schema(description="Получить клиента по ID", summary="Клиент по ID"),
    create=extend_schema(description="Добавить клиента", summary="Добавить клиента"),
    update=extend_schema(description="Обновить запись о клиенте", summary="Обновить запись о клиенте"),
    partial_update=extend_schema(
        description="Обновить запись о клиенте (частично)",
        summary="Обновить запись о клиенте (частично)"
    ),
    destroy=extend_schema(description="Удалить запись клиента", summary="Удалить запись клиента"),
)
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def get_permissions(self):
        """sets permissions for clients' views"""

        permissions = []
        if self.action in ("create", "list", "retrieve"):
            permissions = (IsAuthenticated,)
        elif self.action in ("update", "partial_update", "destroy"):
            permissions = (IsAuthenticated & IsAdminUser,)
        return [permission() for permission in permissions]


@extend_schema_view(
    list=extend_schema(description="Получить список рассылок", summary="Список рассылок"),
    retrieve=extend_schema(description="Получить рассылку по ID", summary="Рассылка по ID"),
    create=extend_schema(
        description="""
Добавить рассылку

Формат фильтра для выбора клиентов для рассылки: **'код оператора 2','код оператора 2'|тэг1,тэг2**

Сначала указываются **коды оператора**, затем символ **|**, затем **тэги**.

Параметры разделяются запятыми.

Чтобы выбрать всех клиентов просто укажите **|** в качестве фильтра
        """,
        summary="Добавить рассылку"
    ),
    update=extend_schema(description="Обновить рассылку", summary="Обновить рассылку"),
    partial_update=extend_schema(
        description="Обновить рассылку (частично)",
        summary="Обновить рассылку (частично)"
    ),
    destroy=extend_schema(description="Удалить рассылку", summary="Удалить рассылку"),
)
class MailingViewSet(viewsets.ModelViewSet):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

    def list(self, request, *args, **kwargs):
        self.serializer_class = MailingListSerializer
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = MailingRetrieveSerializer
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        new_mailing_response = super().create(request, *args, **kwargs)
        new_mailing = Mailing.objects.get(pk=new_mailing_response.data["id"])

        # to execute or schedule the created mailing
        launch_or_schedule_mailing(new_mailing)
        return new_mailing_response

    def get_permissions(self):
        """sets permissions for mailings' views"""

        permissions = []
        if self.action in ("create", "list", "retrieve"):
            permissions = (IsAuthenticated,)
        elif self.action in ("update", "partial_update", "destroy"):
            permissions = (IsAuthenticated & IsAdminUser,)
        return [permission() for permission in permissions]


@extend_schema_view(
    list=extend_schema(description="Получить список сообщений", summary="Список сообщений"),
    retrieve=extend_schema(description="Получить сообщение по ID", summary="Сообщение по ID"),
    create=extend_schema(description="Добавить сообщение", summary="Добавить сообщение"),
    update=extend_schema(description="Обновить сообщение", summary="Обновить сообщение"),
    partial_update=extend_schema(
        description="Обновить сообщение (частично)",
        summary="Обновить сообщение (частично)"
    ),
    destroy=extend_schema(description="Удалить сообщение", summary="Удалить сообщение"),
)
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MsgSerializer

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = MsgRetrieveSerializer
        return super().retrieve(request, *args, **kwargs)

    def get_permissions(self):
        """sets permissions for messages' views"""

        permissions = []
        if self.action in ("list", "retrieve"):
            permissions = (IsAuthenticated,)
        elif self.action in ("create", "update", "partial_update", "destroy"):
            permissions = (IsAuthenticated & IsAdminUser,)
        return [permission() for permission in permissions]


@extend_schema(
    description="Получить список сообщений для заданной рассылки",
    summary="Список сообщений для заданной рассылки",
)
class MessageForMailingView(ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MsgSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        self.queryset = Message.objects.filter(mailing_id=kwargs["mailing_pk"])
        return super().list(request, *args, **kwargs)
