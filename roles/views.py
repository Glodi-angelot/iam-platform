from django.shortcuts import render, redirect, get_object_or_404
from .models import Role
from accounts.decorators import role_required
from logs_app.utils import log_event


SYSTEM_ROLES = ["ADMIN", "AUDITOR", "USER"]


@role_required("can_manage_roles")
def roles_page(request):
    roles = Role.objects.all().order_by("name")
    return render(request, "roles/roles.html", {"roles": roles})


@role_required("can_manage_roles")
def create_role_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description", "")

        can_manage_users = request.POST.get("can_manage_users") == "on"
        can_manage_roles = request.POST.get("can_manage_roles") == "on"
        can_view_logs = request.POST.get("can_view_logs") == "on"
        can_view_kibana = request.POST.get("can_view_kibana") == "on"

        role = Role.objects.create(
            name=name,
            description=description,
            can_manage_users=can_manage_users,
            can_manage_roles=can_manage_roles,
            can_view_logs=can_view_logs,
            can_view_kibana=can_view_kibana,
        )

        log_event(
            request,
            "CREATE_ROLE",
            status="SUCCESS",
            details=f"Rôle créé : {role.name}",
            resource="ROLE"
        )

        return redirect("roles")

    return render(request, "roles/create_role.html")


@role_required("can_manage_roles")
def delete_role_view(request, role_id):
    role = get_object_or_404(Role, id=role_id)

    if role.name in SYSTEM_ROLES:
        log_event(
            request,
            "DELETE_ROLE_FAILED",
            status="FAILED",
            details=f"Tentative de suppression du rôle système : {role.name}",
            resource="ROLE"
        )
        return redirect("roles")

    role_name = role.name
    role.delete()

    log_event(
        request,
        "DELETE_ROLE",
        status="SUCCESS",
        details=f"Rôle supprimé : {role_name}",
        resource="ROLE"
    )

    return redirect("roles")