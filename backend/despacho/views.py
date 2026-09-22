import dataclasses

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from common.api.views import ListCreateView, RetrieveUpdateDestroyView
from common.domain.services import CrudService

from . import serializers
from .domain import entities
from .infrastructure import repositories


class SolicitudListCreateView(ListCreateView):
    service_factory = lambda self: CrudService(repositories.SolicitudRepository())
    serializer_class = serializers.SolicitudSerializer
    entity_class = entities.Solicitud


class SolicitudDetailView(RetrieveUpdateDestroyView):
    service_factory = lambda self: CrudService(repositories.SolicitudRepository())
    serializer_class = serializers.SolicitudSerializer
    entity_class = entities.Solicitud


class IncidenteListCreateView(ListCreateView):
    service_factory = lambda self: CrudService(repositories.IncidenteRepository())
    serializer_class = serializers.IncidenteSerializer
    entity_class = entities.Incidente


class IncidenteDetailView(RetrieveUpdateDestroyView):
    service_factory = lambda self: CrudService(repositories.IncidenteRepository())
    serializer_class = serializers.IncidenteSerializer
    entity_class = entities.Incidente


class IncidenteEstadoUpdateView(APIView):
    def patch(self, request, id):
        servicio = CrudService(repositories.IncidenteRepository())
        actual = servicio.obtener(id)
        if actual is None:
            return Response({'detail': 'Incidente no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.IncidenteEstadoUpdateSerializer(
            actual,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        datos = dataclasses.asdict(actual)
        datos.update(serializer.validated_data)
        entidad_actualizada = entities.Incidente(**datos)
        incidente = servicio.actualizar(id, entidad_actualizada)
        return Response(serializers.IncidenteSerializer(incidente).data)


class RutaListCreateView(ListCreateView):
    service_factory = lambda self: CrudService(repositories.RutaRepository())
    serializer_class = serializers.RutaSerializer
    entity_class = entities.Ruta


class RutaDetailView(RetrieveUpdateDestroyView):
    service_factory = lambda self: CrudService(repositories.RutaRepository())
    serializer_class = serializers.RutaSerializer
    entity_class = entities.Ruta


class UsuarioIncidenteListCreateView(ListCreateView):
    service_factory = lambda self: CrudService(repositories.UsuarioIncidenteRepository())
    serializer_class = serializers.UsuarioIncidenteSerializer
    entity_class = entities.UsuarioIncidente


class UsuarioIncidenteDetailView(RetrieveUpdateDestroyView):
    service_factory = lambda self: CrudService(repositories.UsuarioIncidenteRepository())
    serializer_class = serializers.UsuarioIncidenteSerializer
    entity_class = entities.UsuarioIncidente
