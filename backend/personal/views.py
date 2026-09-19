from common.api.views import ListCreateView, RetrieveUpdateDestroyView
from common.domain.services import CrudService

from . import serializers
from .domain import entities
from .infrastructure import repositories


class DatosConductorListCreateView(ListCreateView):
    service_factory = lambda self: CrudService(repositories.DatosConductorRepository())
    serializer_class = serializers.DatosConductorSerializer
    entity_class = entities.DatosConductor


class DatosConductorDetailView(RetrieveUpdateDestroyView):
    service_factory = lambda self: CrudService(repositories.DatosConductorRepository())
    serializer_class = serializers.DatosConductorSerializer
    entity_class = entities.DatosConductor


class TurnoListCreateView(ListCreateView):
    service_factory = lambda self: CrudService(repositories.TurnoRepository())
    serializer_class = serializers.TurnoSerializer
    entity_class = entities.Turno


class TurnoDetailView(RetrieveUpdateDestroyView):
    service_factory = lambda self: CrudService(repositories.TurnoRepository())
    serializer_class = serializers.TurnoSerializer
    entity_class = entities.Turno
