from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "username", "action", "resource", "status", "ip_address")
    list_filter = ("status", "action", "created_at")
    search_fields = ("username", "action", "resource", "details")
    readonly_fields = ("created_at",)