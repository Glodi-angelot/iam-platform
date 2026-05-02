from django.db import models
from django.contrib.auth.models import User


class AuditLog(models.Model):
    STATUS_CHOICES = [
        ("SUCCESS", "Succès"),
        ("FAILED", "Échec"),
        ("DENIED", "Refusé"),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    username = models.CharField(max_length=150, blank=True)
    action = models.CharField(max_length=100)
    resource = models.CharField(max_length=150, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.action} - {self.status}"