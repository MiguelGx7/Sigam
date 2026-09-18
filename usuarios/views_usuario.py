from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Usuario
from .serializers import UsuarioSerializer


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

    def get(self, request):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)


class CrearUsuario(APIView):

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
