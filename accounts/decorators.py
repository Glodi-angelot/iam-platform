from functools import wraps
from django.shortcuts import redirect
from logs_app.utils import log_event


def role_required(permission_name):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")

            profile = getattr(request.user, "profile", None)

            if not profile or not profile.role:
                log_event(request, "ACCESS_DENIED", status="DENIED", details="No role assigned")
                return redirect("access_denied")

            has_permission = getattr(profile.role, permission_name, False)

            if not has_permission:
                log_event(request, "ACCESS_DENIED", status="DENIED", details=f"Missing permission: {permission_name}")
                return redirect("access_denied")

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator