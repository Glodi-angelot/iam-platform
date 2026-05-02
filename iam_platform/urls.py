from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

# Import des vues principales
from users_app.views import users_page, create_user_view, edit_user_view, delete_user_view, profile_view
from users_app.views import edit_user_view
from roles.views import roles_page, create_role_view, delete_role_view
from logs_app.views import logs_page
from .views import home_view, dashboard_view, kibana_view, error_403_view


urlpatterns = [
    # Admin Django
    path('admin/', admin.site.urls),

    # Redirection page d’accueil → login
    path('', home_view, name='home'),

    # Accounts (login, logout, access denied)
    path('', include('accounts.urls')),

    # Dashboard
    path('dashboard/', dashboard_view, name='dashboard'),

    # Modules IAM
    path('users/', users_page, name='users'),
    path('users/create/', create_user_view, name='create_user'),
    path('users/delete/<int:user_id>/', delete_user_view, name='delete_user'),
    path('users/edit/<int:user_id>/', edit_user_view, name='edit_user'),
    path('roles/', roles_page, name='roles'),
    path('roles/create/', create_role_view, name='create_role'),
    path('roles/delete/<int:role_id>/', delete_role_view, name='delete_role'),
    path('logs/', logs_page, name='logs'),
    path('profile/', profile_view, name='profile'),

    # Monitoring Kibana
    path('kibana/', kibana_view, name='kibana'),

    # Page erreur
    path('403/', error_403_view, name='error_403'),

    
]