from django.contrib import admin

# Register your models here.
from .models import ContactMessage, BloodRequest, Stock, SidebarItem

admin.site.register(Stock)
admin.site.register(BloodRequest)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'created_at')
    search_fields = ('name', 'email')
