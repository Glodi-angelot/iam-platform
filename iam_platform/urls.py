from django.contrib import admin
from django.urls import path
from accounts.views import login_view
from users_app.views import users_page
from roles.views import roles_page
from logs_app.views import logs_page
from .views import dashboard_view, kibana_view, error_403_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='home'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('users/', users_page, name='users'),
    path('roles/', roles_page, name='roles'),
    path('logs/', logs_page, name='logs'),
    path('kibana/', kibana_view, name='kibana'),
    path('403/', error_403_view, name='error_403'),
]