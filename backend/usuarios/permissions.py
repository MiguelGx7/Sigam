from rest_framework.permissions import BasePermission


class EsSuperAdministrador(BasePermission):
    """Permite esta accion solo al superadministrador del sistema."""

    message = 'Solo el Super Administrador puede cambiar contraseñas de otros usuarios.'

    def has_permission(self, request, view):
        usuario = request.user

        if not usuario or not usuario.is_authenticated:
            return False

        if usuario.is_superuser:
            return True

        return bool(usuario.rol and usuario.rol.nombre == 'Super Administrador')
