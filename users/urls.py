from django.urls import include, path
from djoser.views import UserViewSet
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

users_router = SimpleRouter()

users_router.register("users", UserViewSet, basename="users")

urlpatterns = [
    path("refresh/", TokenRefreshView.as_view()),
    path("token/", TokenObtainPairView.as_view()),
    path("", include(users_router.urls)),
]
