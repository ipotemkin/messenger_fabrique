from django.contrib import admin
from mailing.models import Mailing, Client, Message

admin.site.register(Mailing)
admin.site.register(Client)
admin.site.register(Message)
