from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class ListCreateView(APIView):
    """GET lista / POST crea. Subclases fijan service_factory, serializer_class y entity_class."""

    service_factory = None
    serializer_class = None
    entity_class = None

    def get(self, request):
        servicio = self.service_factory()
        datos = self.serializer_class(servicio.listar(), many=True).data
        return Response(datos)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        servicio = self.service_factory()
        entidad = self.entity_class(id=None, **serializer.validated_data)
        try:
            creada = servicio.crear(entidad)
        except IntegrityError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_409_CONFLICT)
        return Response(self.serializer_class(creada).data, status=status.HTTP_201_CREATED)


class RetrieveUpdateDestroyView(APIView):
    """GET detalle / PUT actualiza / DELETE elimina, por id."""

    service_factory = None
    serializer_class = None
    entity_class = None

    def get(self, request, id):
        servicio = self.service_factory()
        entidad = servicio.obtener(id)
        if entidad is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(self.serializer_class(entidad).data)

    def put(self, request, id):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        servicio = self.service_factory()
        entidad = self.entity_class(id=id, **serializer.validated_data)
        try:
            actualizada = servicio.actualizar(id, entidad)
        except IntegrityError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_409_CONFLICT)
        return Response(self.serializer_class(actualizada).data)

    def delete(self, request, id):
        servicio = self.service_factory()
        try:
            servicio.eliminar(id)
        except IntegrityError:
            return Response(
                {'detail': 'No se puede eliminar: otros registros dependen de este.'},
                status=status.HTTP_409_CONFLICT,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
