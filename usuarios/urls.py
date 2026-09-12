from django.urls import path
from usuarios.views_login import login_usuario, inicio, logout_usuario
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', login_usuario, name='login'),
    path('inicio/', inicio, name='inicio'),
    path('logout/', logout_usuario, name='logout'),
    path('recuperar/', auth_views.PasswordResetView.as_view(template_name='usuarios/recuperar_temp.html'), name='password_reset'),
]