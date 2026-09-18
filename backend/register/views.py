from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .serializer import UsuarioSerializer

class RegisterView(APIView):
    @swagger_auto_schema(
        tags=['registro'],
        request_body=UsuarioSerializer,
        responses={201: UsuarioSerializer}
    )
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Usuario registrado exitosamente"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)