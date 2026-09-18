from django.contrib.auth import views as auth_views
from django.urls import path

from usuarios.views_login import inicio, login_usuario, logout_usuario
from usuarios.views_roles import (
    rol_api_detail, roles_api, roles_create, roles_delete, roles_edit, roles_list,
)
from usuarios.views_usuario import CrearUsuario, LeerUsuarios

urlpatterns = [
    path('login/', login_usuario, name='login'),
    path('inicio/', inicio, name='inicio'),
    path('logout/', logout_usuario, name='logout'),
    path('recuperar/', auth_views.PasswordResetView.as_view(template_name='usuarios/recuperar_temp.html'), name='password_reset'),
    path('roles/', roles_list, name='roles_list'),
    path('roles/nuevo/', roles_create, name='roles_create'),
    path('roles/editar/<int:id_rol>/', roles_edit, name='roles_edit'),
    path('roles/eliminar/<int:id_rol>/', roles_delete, name='roles_delete'),
    path('api/roles/', roles_api, name='roles_api'),
    path('api/roles/<int:id_rol>/', rol_api_detail, name='rol_api_detail'),
    path('usuarios/', LeerUsuarios.as_view(), name='usuarios_listar'),
    path('usuarios/crear/', CrearUsuario.as_view(), name='usuarios_crear'),
    path('usuarios/editar/<int:id>/', CrearUsuario.as_view(), name='usuarios_editar'),
    path('usuarios/eliminar/<int:id>/', CrearUsuario.as_view(), name='usuarios_eliminar'),
]
