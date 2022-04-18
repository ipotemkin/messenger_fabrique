from django.contrib.messages.storage.cookie import MessageSerializer
from django.shortcuts import render
from rest_framework import viewsets

from mailing.models import Client, Mailing, Message
from mailing.serializers import ClientSerializer, MailingSerializer, MsgSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MailingViewSet(viewsets.ModelViewSet):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MsgSerializer
