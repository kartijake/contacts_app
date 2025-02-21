from django.contrib import admin
from .models import Contact, Telephone

class TelephoneInline(admin.TabularInline):
    model = Telephone
    extra = 1  # Allows adding multiple numbers in the admin panel

class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "city", "country", "created_at")
    search_fields = ("name", "user__email", "city", "country")
    list_filter = ("country", "created_at")
    inlines = [TelephoneInline]

admin.site.register(Contact, ContactAdmin)
admin.site.register(Telephone)
