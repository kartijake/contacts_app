from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.user_auth.urls")),
    path("api/contacts", include("apps.contacts.urls")),
]
