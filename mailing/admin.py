from django.contrib import admin
from mailing.models import Mailing, Client, Message


class MsgAdmin(admin.ModelAdmin):
    list_display = ('pk', 'created_at', 'status', 'client', 'mailing')
    # list_display_links = ('name', 'author')
    # search_fields = ('name', 'author', 'description')


admin.site.register(Mailing)
admin.site.register(Client)
admin.site.register(Message, MsgAdmin)
