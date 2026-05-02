from django.contrib import admin
from .models import Role


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "can_manage_users",
        "can_manage_roles",
        "can_view_logs",
        "can_view_kibana",
        "created_at",
    )
    search_fields = ("name",)