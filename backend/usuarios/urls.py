from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from usuarios.views_login import LoginView
from usuarios.views_password import RecuperarPasswordView, ConfirmarPasswordView
from usuarios.views_roles import RolListCreateView, RolDetailView
from usuarios.views_usuario import CrearUsuario, LeerUsuarios, lista_usuarios, detalle_usuario, crear_usuario_html


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('password/recuperar/', RecuperarPasswordView.as_view(), name='password_recuperar'),
    path('password/confirmar/', ConfirmarPasswordView.as_view(), name='password_confirmar'),

    path('roles/', RolListCreateView.as_view(), name='roles_list_create'),
    path('roles/<int:id_rol>/', RolDetailView.as_view(), name='roles_detail'),

    path('usuarios/', LeerUsuarios.as_view(), name='usuarios_listar'),
    path('usuarios/lista/', lista_usuarios, name='usuarios_lista'),
    path('usuarios/nuevo/', crear_usuario_html, name='usuario_crear_html'),
    path('usuarios/crear/', CrearUsuario.as_view(), name='usuarios_crear'),
    path('usuarios/editar/<int:id>/', CrearUsuario.as_view(), name='usuarios_editar'),
    path('usuarios/eliminar/<int:id>/', CrearUsuario.as_view(), name='usuarios_eliminar'),
    path('usuarios/detalle/<int:id>/', detalle_usuario, name='usuarios_detalle'),

]