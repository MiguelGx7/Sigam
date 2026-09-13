from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Usuario
from .serializers import UsuarioSerializer

class LeerUsuarios(APIView):
    def get(self, request):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)


class CrearUsuario(APIView):
    def post(self,request):
        serializer=UsuarioSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)