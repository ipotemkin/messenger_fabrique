from django.contrib import admin
from mailing.models import Mailing, Client, Message


class MsgAdmin(admin.ModelAdmin):
    list_display = ('pk', 'created_at', 'status', 'client', 'mailing')


class MailingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'mailing_filter', 'launch_at', 'terminate_at')


class ClientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'phone', 'operator_id', 'tag', 'timezone')


admin.site.register(Mailing, MailingAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Message, MsgAdmin)
