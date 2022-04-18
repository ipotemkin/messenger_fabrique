from django.db.models import Count
from rest_framework import serializers

from mailing.models import Client, Mailing, Message


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        # exclude = ("id",)
        fields = "__all__"


class MsgSimpleSerializer(serializers.ModelSerializer):
    # client = ClientSerializer()
    # mailing = MailingSerializer()

    class Meta:
        model = Message
        # exclude = ("id",)
        # fields = ("status",)
        fields = "__all__"


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = "__all__"


class MailingRetrieveSerializer(MailingSerializer):
    messages = MsgSimpleSerializer(many=True)


class MailingListSerializer(MailingSerializer):
    messages_stats = serializers.SerializerMethodField()

    def get_messages_stats(self, obj):
        statuses = (
            Message.objects
            .filter(mailing=obj.pk)
            .values('status')
            .annotate(counts=Count('status'))
        )
        return [{status['status']: status['counts']} for status in statuses]


class MsgSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    mailing = MailingSerializer()

    class Meta:
        model = Message
        # exclude = ("id",)
        # fields = ("status",)
        fields = "__all__"
