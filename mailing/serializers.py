from django.db.models import Count
from rest_framework import serializers

from mailing.models import Client, Mailing, Message


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = "__all__"


class MsgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class MsgRetrieveSerializer(MsgSerializer):
    client = ClientSerializer()
    mailing = MailingSerializer()


class MailingRetrieveSerializer(MailingSerializer):
    messages = MsgSerializer(many=True)


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
