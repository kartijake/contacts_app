from django.urls import path
from .views import ContactView, SearchContactsView

urlpatterns = [
    path("", ContactView.as_view(), name="contacts"),
    path("/<int:contact_id>", ContactView.as_view(), name="contacts"),
    path("/search", SearchContactsView.as_view(), name="search-contacts")
]
