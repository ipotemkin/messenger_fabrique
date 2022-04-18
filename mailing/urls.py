from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from mailing.views import (
    ClientViewSet,
    MailingViewSet,
    MessageViewSet,
    MessageForMailingView
)

router = DefaultRouter()  # SimpleRouter
router.register('clients', ClientViewSet)
router.register('messages', MessageViewSet)
router.register('mailings', MailingViewSet)


urlpatterns = [
    re_path(r'mailings/(?P<mailing_pk>\d+)/messages', MessageForMailingView.as_view()),
    path("", include(router.urls)),
]
