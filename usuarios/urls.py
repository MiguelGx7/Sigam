from django.urls import path
from django.contrib.auth import views as auth_views

from usuarios.views_login import login_usuario, inicio, logout_usuario
from usuarios.views_roles import roles_edit, roles_delete
from usuarios.views_usuario import CrearUsuario, LeerUsuarios, lista_usuarios, detalle_usuario, crear_usuario_html


urlpatterns = [
    path('login/', login_usuario, name='login'),
    path('inicio/', inicio, name='inicio'),
    path('logout/', logout_usuario, name='logout'),
    path('recuperar/', auth_views.PasswordResetView.as_view(template_name='usuarios/recuperar_temp.html'), name='password_reset'),

    path('roles/editar/<int:id_rol>/', roles_edit, name='roles_edit'),
    path('roles/eliminar/<int:id_rol>/', roles_delete, name='roles_delete'),

    path('usuarios/', LeerUsuarios.as_view(), name='usuarios_listar'),
    path('usuarios/lista/', lista_usuarios, name='usuarios_lista'),
    path('usuarios/nuevo/', crear_usuario_html, name='usuario_crear_html'),
    path('usuarios/crear/', CrearUsuario.as_view(), name='usuarios_crear'),
    path('usuarios/editar/<int:id>/', CrearUsuario.as_view(), name='usuarios_editar'),
    path('usuarios/eliminar/<int:id>/', CrearUsuario.as_view(), name='usuarios_eliminar'),
    path('usuarios/detalle/<int:id>/', detalle_usuario, name='usuarios_detalle'),
    
]