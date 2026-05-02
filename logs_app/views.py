from django.shortcuts import render
from accounts.decorators import role_required
from .models import AuditLog


@role_required("can_view_logs")
def logs_page(request):
    logs = AuditLog.objects.all()[:100]
    return render(request, "logs_app/logs.html", {"logs": logs})