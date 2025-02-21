from django.urls import path
from .views import RegisterUserView,LoginUserView,CustomTokenRefreshView
urlpatterns = [
    path("register", RegisterUserView.as_view(), name="user-register"),
     path("login", LoginUserView.as_view(), name="user-login"),
    path("refresh", CustomTokenRefreshView.as_view(), name="token-refresh")
]
