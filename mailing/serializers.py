from rest_framework import serializers

from mailing.models import Client, Mailing, Message


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        # exclude = ("id",)
        fields = "__all__"


class MailingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mailing
        # exclude = ("id",)
        fields = "__all__"


class MsgSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    mailing = MailingSerializer()

    class Meta:
        model = Message
        # exclude = ("id",)
        # fields = ("status",)
        fields = "__all__"
