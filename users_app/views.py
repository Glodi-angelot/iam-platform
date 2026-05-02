from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from roles.models import Role
from users_app.models import UserProfile
from accounts.decorators import role_required
from logs_app.utils import log_event
from django.contrib.auth.decorators import login_required


# LISTE DES UTILISATEURS
@role_required("can_manage_users")
def users_page(request):
    users = User.objects.all().order_by("-date_joined")
    return render(request, "users_app/users.html", {"users": users})


# CRÉATION UTILISATEUR
@role_required("can_manage_users")
def create_user_view(request):
    roles = Role.objects.all()

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role_id = request.POST.get("role")

        role = Role.objects.get(id=role_id)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        UserProfile.objects.create(user=user, role=role)

        log_event(
            request,
            "CREATE_USER",
            status="SUCCESS",
            details=f"Utilisateur créé : {username}",
            resource="USER"
        )

        return redirect("users")

    return render(request, "users_app/create_user.html", {"roles": roles})


# MODIFICATION UTILISATEUR
@role_required("can_manage_users")
def edit_user_view(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    roles = Role.objects.all()
    profile, _ = UserProfile.objects.get_or_create(user=user_obj)

    if request.method == "POST":
        old_email = user_obj.email
        old_role = profile.role.name if profile.role else "Aucun rôle"
        old_active = user_obj.is_active
        old_staff = user_obj.is_staff

        email = request.POST.get("email", "")
        role_id = request.POST.get("role")

        user_obj.email = email
        user_obj.is_active = request.POST.get("is_active") == "on"
        user_obj.is_staff = request.POST.get("is_staff") == "on"

        if role_id:
            role = get_object_or_404(Role, id=role_id)
            profile.role = role
        else:
            role = None
            profile.role = None

        user_obj.save()
        profile.save()

        new_role = role.name if role else "Aucun rôle"

        details = (
            f"Utilisateur modifié : {user_obj.username} | "
            f"email: {old_email} → {user_obj.email} | "
            f"rôle: {old_role} → {new_role} | "
            f"actif: {old_active} → {user_obj.is_active} | "
            f"staff: {old_staff} → {user_obj.is_staff}"
        )

        log_event(
            request,
            "UPDATE_USER",
            status="SUCCESS",
            details=details,
            resource="USER"
        )

        return redirect("users")

    return render(request, "users_app/edit_user.html", {
        "user_obj": user_obj,
        "roles": roles,
        "profile": profile
    })


# SUPPRESSION UTILISATEUR
@role_required("can_manage_users")
def delete_user_view(request, user_id):
    user_to_delete = get_object_or_404(User, id=user_id)

    # Empêcher suppression de soi-même
    if request.user.id == user_to_delete.id:
        log_event(
            request,
            "DELETE_USER_FAILED",
            status="FAILED",
            details="Tentative de suppression de son propre compte",
            resource="USER"
        )
        return redirect("users")

    username = user_to_delete.username
    user_to_delete.delete()

    log_event(
        request,
        "DELETE_USER",
        status="SUCCESS",
        details=f"Utilisateur supprimé : {username}",
        resource="USER"
    )

    return redirect("users")



# Pour profil utilisateur
@login_required(login_url="login")
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    log_event(
        request,
        "VIEW_PROFILE",
        status="SUCCESS",
        details=f"Consultation du profil : {request.user.username}",
        resource="PROFILE"
    )

    return render(request, "users_app/profile.html", {
        "profile": profile
    })