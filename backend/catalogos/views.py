from common.api.views import ListCreateView, RetrieveUpdateDestroyView
from common.domain.services import CrudService

from . import serializers
from .domain import entities
from .infrastructure import repositories


class PrioridadListCreateView(ListCreateView):
    service_factory = lambda self: CrudService(repositories.PrioridadRepository())
    serializer_class = serializers.PrioridadSerializer
    entity_class = entities.Prioridad


class PrioridadDetailView(RetrieveUpdateDestroyView):
    service_factory = lambda self: CrudService(repositories.PrioridadRepository())
    serializer_class = serializers.PrioridadSerializer
    entity_class = entities.Prioridad


class EstadoSolicitudListCreateView(ListCreateView):
    service_factory = lambda self: CrudService(repositories.EstadoSolicitudRepository())
    serializer_class = serializers.EstadoSolicitudSerializer
    entity_class = entities.EstadoSolicitud


class EstadoSolicitudDetailView(RetrieveUpdateDestroyView):
    service_factory = lambda self: CrudService(repositories.EstadoSolicitudRepository())
    serializer_class = serializers.EstadoSolicitudSerializer
    entity_class = entities.EstadoSolicitud


class EstadoTipoIncidenteListCreateView(ListCreateView):
    service_factory = lambda self: CrudService(repositories.EstadoTipoIncidenteRepository())
    serializer_class = serializers.EstadoTipoIncidenteSerializer
    entity_class = entities.EstadoTipoIncidente


class EstadoTipoIncidenteDetailView(RetrieveUpdateDestroyView):
    service_factory = lambda self: CrudService(repositories.EstadoTipoIncidenteRepository())
    serializer_class = serializers.EstadoTipoIncidenteSerializer
    entity_class = entities.EstadoTipoIncidente


class TipoCentroListCreateView(ListCreateView):
    service_factory = lambda self: CrudService(repositories.TipoCentroRepository())
    serializer_class = serializers.TipoCentroSerializer
    entity_class = entities.TipoCentro


class TipoCentroDetailView(RetrieveUpdateDestroyView):
    service_factory = lambda self: CrudService(repositories.TipoCentroRepository())
    serializer_class = serializers.TipoCentroSerializer
    entity_class = entities.TipoCentro


class TipoAmbulanciaListCreateView(ListCreateView):
    service_factory = lambda self: CrudService(repositories.TipoAmbulanciaRepository())
    serializer_class = serializers.TipoAmbulanciaSerializer
    entity_class = entities.TipoAmbulancia


class TipoAmbulanciaDetailView(RetrieveUpdateDestroyView):
    service_factory = lambda self: CrudService(repositories.TipoAmbulanciaRepository())
    serializer_class = serializers.TipoAmbulanciaSerializer
    entity_class = entities.TipoAmbulancia


class EstadoAmbulanciaListCreateView(ListCreateView):
    service_factory = lambda self: CrudService(repositories.EstadoAmbulanciaRepository())
    serializer_class = serializers.EstadoAmbulanciaSerializer
    entity_class = entities.EstadoAmbulancia


class EstadoAmbulanciaDetailView(RetrieveUpdateDestroyView):
    service_factory = lambda self: CrudService(repositories.EstadoAmbulanciaRepository())
    serializer_class = serializers.EstadoAmbulanciaSerializer
    entity_class = entities.EstadoAmbulancia


class TipoIncidenteListCreateView(ListCreateView):
    service_factory = lambda self: CrudService(repositories.TipoIncidenteRepository())
    serializer_class = serializers.TipoIncidenteSerializer
    entity_class = entities.TipoIncidente


class TipoIncidenteDetailView(RetrieveUpdateDestroyView):
    service_factory = lambda self: CrudService(repositories.TipoIncidenteRepository())
    serializer_class = serializers.TipoIncidenteSerializer
    entity_class = entities.TipoIncidente
