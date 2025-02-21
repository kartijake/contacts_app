from django.urls import path
from .views import ContactListView, SearchContactsView,ContactDetailView

urlpatterns = [
    path("", ContactListView.as_view(), name="contacts"),
    path("/<int:contact_id>", ContactDetailView.as_view(), name="contacts"),
    path("/search", SearchContactsView.as_view(), name="search-contacts")
]
