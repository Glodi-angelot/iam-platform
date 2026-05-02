from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required


# Page d'accueil publique
def home_view(request):
    return render(request, "home.html")


# Dashboard (connexion obligatoire)
@login_required(login_url="login")
def dashboard_view(request):
    return render(request, "dashboard/dashboard.html")


# Accès Kibana (protégé par rôle)
@role_required("can_view_kibana")
def kibana_view(request):
    return render(request, "monitoring/kibana.html")


# Page erreur 403
def error_403_view(request):
    return render(request, "errors/403.html", status=403)