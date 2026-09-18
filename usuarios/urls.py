from django.urls import path
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenRefreshView
from usuarios.views_login import LoginView
from usuarios.views_roles import roles_edit, roles_delete
from usuarios.views_usuario import CrearUsuario, LeerUsuarios

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('roles/editar/<int:id_rol>/', roles_edit, name='roles_edit'),
    path('roles/eliminar/<int:id_rol>/', roles_delete, name='roles_delete'),

    path('usuarios/', LeerUsuarios.as_view(), name='usuarios_listar'),
    path('usuarios/crear/', CrearUsuario.as_view(), name='usuarios_crear'),
    path('usuarios/editar/<int:id>/', CrearUsuario.as_view(), name='usuarios_editar'),
    path('usuarios/eliminar/<int:id>/', CrearUsuario.as_view(), name='usuarios_eliminar'),
]