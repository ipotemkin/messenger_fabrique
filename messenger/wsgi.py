"""
WSGI config for messenger project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from mailing.tasks import set_tasks_on_startup

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messenger.settings')

application = get_wsgi_application()

set_tasks_on_startup.apply_async(countdown=10)
