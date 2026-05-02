from django.contrib.auth.models import User
from roles.models import Role
from users_app.models import UserProfile

users_data = [
    ("admin_iam", "admin@iam.local", "Admin12345", "ADMIN", True, True),
    ("auditeur_iam", "auditeur@iam.local", "Auditeur12345", "AUDITOR", False, False),
    ("user_iam", "user@iam.local", "User12345", "USER", False, False),
]

for username, email, password, role_name, is_staff, is_superuser in users_data:
    role = Role.objects.get(name=role_name)

    user, created = User.objects.get_or_create(username=username)
    user.email = email
    user.is_staff = is_staff
    user.is_superuser = is_superuser
    user.set_password(password)
    user.save()

    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.role = role
    profile.save()

    print(f"{username} -> {role_name}")

print("Utilisateurs de simulation créés avec succès.")