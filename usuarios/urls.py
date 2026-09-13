from django.urls import path
from usuarios.views_login import login_usuario, inicio, logout_usuario
from django.contrib.auth import views as auth_views
from usuarios.views_roles import roles_edit, roles_delete  # <--- Importas tus funciones

urlpatterns = [
    # Rutas existentes del equipo
    path('login/', login_usuario, name='login'),
    path('inicio/', inicio, name='inicio'),
    path('logout/', logout_usuario, name='logout'),
    path('recuperar/', auth_views.PasswordResetView.as_view(template_name='usuarios/recuperar_temp.html'), name='password_reset'),
    
    path('roles/editar/<int:id_rol>/', roles_edit, name='roles_edit'),
    path('roles/eliminar/<int:id_rol>/', roles_delete, name='roles_delete'),
]
