from django.urls import path
from .views import RegisterUserView,LoginUserView
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path("register", RegisterUserView.as_view(), name="user-register"),
     path("login", LoginUserView.as_view(), name="user-login"),
    path("refresh", TokenRefreshView.as_view(), name="token-refresh")
]
