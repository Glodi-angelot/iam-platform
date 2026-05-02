from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from logs_app.utils import log_event


def login_view(request):
    if request.user.is_authenticated:
        profile = getattr(request.user, "profile", None)

        if profile and profile.role and profile.role.name in ["ADMIN", "AUDITOR"]:
            return redirect("dashboard")

        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            log_event(request, "LOGIN_SUCCESS")

            profile = getattr(user, "profile", None)

            if profile and profile.role and profile.role.name in ["ADMIN", "AUDITOR"]:
                return redirect("dashboard")

            return redirect("home")

        log_event(
            request,
            "LOGIN_FAILED",
            status="FAILED",
            details="Identifiants incorrects"
        )
        return render(
            request,
            "accounts/login.html",
            {"error": "Identifiants incorrects"}
        )

    return render(request, "accounts/login.html")


def logout_view(request):
    log_event(request, "LOGOUT")
    logout(request)
    return redirect("home")


def access_denied_view(request):
    return render(request, "accounts/access_denied.html")