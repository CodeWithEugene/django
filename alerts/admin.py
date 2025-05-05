from django.contrib import admin
from .models import Alert

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'user', 'created_at', 'is_read')
    list_filter = ('level', 'is_read', 'created_at')
    search_fields = ('title', 'message', 'user__username')