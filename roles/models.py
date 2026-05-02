from django.db import models


class Role(models.Model):
    ROLE_CHOICES = [
        ("ADMIN", "Administrateur"),
        ("AUDITOR", "Auditeur"),
        ("USER", "Utilisateur"),
    ]

    name = models.CharField(max_length=30, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True)

    can_manage_users = models.BooleanField(default=False)
    can_manage_roles = models.BooleanField(default=False)
    can_view_logs = models.BooleanField(default=False)
    can_view_kibana = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.get_name_display()