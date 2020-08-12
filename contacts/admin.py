from django.contrib import admin
from .models import Contact


class ContactsAdmin(admin.ModelAdmin):
    list_display = ('listing_id', 'listing', 'name', 'email', 'phone', 'contact_date', 'user_id')
    list_display_links = ('name', 'email', 'listing')
    search_fields = ('name', 'email', 'phone')
    list_per_page = 25


admin.site.register(Contact, ContactsAdmin)
