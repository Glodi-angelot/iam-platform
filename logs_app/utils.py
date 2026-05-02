import json
import os
from datetime import datetime
from django.conf import settings
from .models import AuditLog


def log_event(request, action, status="SUCCESS", details="", resource="AUTH"):
    user = request.user if request.user.is_authenticated else None
    ip_address = get_client_ip(request)
    user_agent = request.META.get("HTTP_USER_AGENT", "")

    # 1. Enregistrement dans la base de données Django
    audit_log = AuditLog.objects.create(
        user=user,
        username=user.username if user else "",
        action=action,
        resource=resource,
        ip_address=ip_address,
        user_agent=user_agent,
        status=status,
        details=details,
    )

    # 2. Écriture dans un fichier JSON pour Elasticsearch/Kibana
    write_json_log(audit_log, user_agent)


def write_json_log(audit_log, user_agent):
    logs_dir = os.path.join(settings.BASE_DIR, "logs")
    os.makedirs(logs_dir, exist_ok=True)

    log_file_path = os.path.join(logs_dir, "iam_audit.log")

    log_data = {
        "@timestamp": datetime.utcnow().isoformat() + "Z",
        "event": {
            "action": audit_log.action,
            "status": audit_log.status,
            "resource": audit_log.resource,
        },
        "user": {
            "name": audit_log.username if audit_log.username else "anonymous",
        },
        "source": {
            "ip": str(audit_log.ip_address) if audit_log.ip_address else "",
        },
        "user_agent": {
            "original": user_agent,
        },
        "message": audit_log.details,
        "application": "iam_platform",
    }

    with open(log_file_path, "a", encoding="utf-8") as file:
        file.write(json.dumps(log_data, ensure_ascii=False) + "\n")


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    return request.META.get("REMOTE_ADDR")