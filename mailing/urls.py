from django.urls import include, path
from rest_framework.routers import DefaultRouter

from mailing.views import ClientViewSet, MailingViewSet, MessageViewSet

router = DefaultRouter()  # SimpleRouter
router.register('clients', ClientViewSet)
router.register('messages', MessageViewSet)
router.register('mailings', MailingViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
