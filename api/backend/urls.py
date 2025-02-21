# from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    # path("admin/", admin.site.urls),
    path("api/auth/", include("apps.user_auth.urls")),
    path("api/contacts", include("apps.contacts.urls")),
    path("api/schema", SpectacularAPIView.as_view(), name="schema"),
    path("api/redoc", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("api/docs", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
