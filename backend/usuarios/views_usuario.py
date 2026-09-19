from django.shortcuts import render

from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import SolicitudCambioPassword, Usuario
from .permissions import EsSuperAdministrador
from .serializers import SolicitudCambioPasswordSerializer, UsuarioSerializer


def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(
        request,
        'usuarios/usuario_list.html',
        {'usuarios': usuarios}
    )

def detalle_usuario(request, id):
    usuario = Usuario.objects.get(id=id)
    return render(
        request,
        'usuarios/usuario_detail.html',
        {'usuario': usuario}
    )
def crear_usuario_html(request):
    return render(request, 'usuarios/usuario_crear.html')

class LeerUsuarios(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)


class CrearUsuario(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def put(self, request, id):
        try:
            usuario = Usuario.objects.get(id=id)
        except Usuario.DoesNotExist:
            return Response(
                {'error': 'Usuario no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = UsuarioSerializer(
            usuario,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, id):
        try:
            usuario = Usuario.objects.get(id=id)
        except Usuario.DoesNotExist:
            return Response(
                {'error': 'Usuario no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )

        usuario.delete()

        return Response(
            {'mensaje': 'Usuario eliminado correctamente'},
            status=status.HTTP_204_NO_CONTENT
        )


class CambiarPasswordAdministrativaView(APIView):
    """Permite al Super Administrador restablecer la clave de un usuario."""
    permission_classes = [EsSuperAdministrador]

    def post(self, request, id):
        nueva_password = request.data.get('password', '')

        if len(nueva_password) < 6:
            return Response(
                {'password': 'La contraseña debe tener al menos 6 caracteres.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            usuario = Usuario.objects.get(id=id)
        except Usuario.DoesNotExist:
            return Response(
                {'error': 'Usuario no encontrado'},
                status=status.HTTP_404_NOT_FOUND,
            )

        usuario.set_password(nueva_password)
        usuario.save(update_fields=['password'])
        SolicitudCambioPassword.objects.filter(usuario=usuario, atendida=False).update(
            atendida=True,
            atendida_en=timezone.now(),
        )

        return Response({'mensaje': 'Contraseña actualizada correctamente.'})


class SolicitudesCambioPasswordView(APIView):
    """Lista las solicitudes pendientes que debe atender el Super Administrador."""
    permission_classes = [EsSuperAdministrador]

    def get(self, request):
        solicitudes = SolicitudCambioPassword.objects.filter(atendida=False).select_related('usuario')
        return Response(SolicitudCambioPasswordSerializer(solicitudes, many=True).data)


class CambiarPasswordAdministrativaView(APIView):
    """Permite al Super Administrador restablecer la clave de un usuario."""
    permission_classes = [EsSuperAdministrador]

    def post(self, request, id):
        nueva_password = request.data.get('password', '')

        if len(nueva_password) < 6:
            return Response(
                {'password': 'La contraseña debe tener al menos 6 caracteres.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            usuario = Usuario.objects.get(id=id)
        except Usuario.DoesNotExist:
            return Response(
                {'error': 'Usuario no encontrado'},
                status=status.HTTP_404_NOT_FOUND,
            )

        usuario.set_password(nueva_password)
        usuario.save(update_fields=['password'])

        return Response({'mensaje': 'Contraseña actualizada correctamente.'})
