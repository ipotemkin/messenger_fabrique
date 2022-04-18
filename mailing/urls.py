from django.urls import include, path
from rest_framework.routers import DefaultRouter

from mailing.views import ClientViewSet, MailingViewSet, MessageViewSet, MailingsStatsView

router = DefaultRouter()  # SimpleRouter
router.register('clients', ClientViewSet)
router.register('messages', MessageViewSet)
router.register('mailings', MailingViewSet)
router.register(r'mailings/(?P<mailing_pk>\d+)/messages', MessageViewSet)


urlpatterns = [
    path("mailings/stats/", MailingsStatsView.as_view()),
    path("", include(router.urls)),
]
