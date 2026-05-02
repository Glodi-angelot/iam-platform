from django.urls import path
from .views import login_view, logout_view, access_denied_view

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("access-denied/", access_denied_view, name="access_denied"),
]