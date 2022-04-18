from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from mailing.models import Client, Mailing, Message
from mailing.serializers import (
    ClientSerializer,
    MailingSerializer,
    MsgSerializer,
    MsgRetrieveSerializer,
    MailingListSerializer,
    MailingRetrieveSerializer
)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MailingViewSet(viewsets.ModelViewSet):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

    def list(self, request, *args, **kwargs):
        self.serializer_class = MailingListSerializer
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = MailingRetrieveSerializer
        return super().retrieve(request, *args, **kwargs)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MsgSerializer

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = MsgRetrieveSerializer
        return super().retrieve(request, *args, **kwargs)


class MessageForMailingView(ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MsgSerializer

    def list(self, request, *args, **kwargs):
        self.queryset = Message.objects.filter(mailing_id=kwargs["mailing_pk"])
        return super().list(request, *args, **kwargs)
