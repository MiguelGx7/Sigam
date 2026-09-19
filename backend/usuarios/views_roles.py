from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Rol
from .serializers import RolSerializer


class RolListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        roles = Rol.objects.all()
        return Response(RolSerializer(roles, many=True).data)

    def post(self, request):
        serializer = RolSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RolDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id_rol):
        try:
            rol = Rol.objects.get(id_rol=id_rol)
        except Rol.DoesNotExist:
            return Response({'error': 'Rol no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        return Response(RolSerializer(rol).data)

    def put(self, request, id_rol):
        try:
            rol = Rol.objects.get(id_rol=id_rol)
        except Rol.DoesNotExist:
            return Response({'error': 'Rol no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = RolSerializer(rol, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id_rol):
        try:
            rol = Rol.objects.get(id_rol=id_rol)
        except Rol.DoesNotExist:
            return Response({'error': 'Rol no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        rol.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
