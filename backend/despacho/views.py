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
