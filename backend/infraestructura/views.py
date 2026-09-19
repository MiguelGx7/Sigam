from common.api.views import ListCreateView, RetrieveUpdateDestroyView
from common.domain.services import CrudService

from . import serializers
from .domain import entities
from .infrastructure import repositories


class CentroSaludListCreateView(ListCreateView):
    service_factory = lambda self: CrudService(repositories.CentroSaludRepository())
    serializer_class = serializers.CentroSaludSerializer
    entity_class = entities.CentroSalud


class CentroSaludDetailView(RetrieveUpdateDestroyView):
    service_factory = lambda self: CrudService(repositories.CentroSaludRepository())
    serializer_class = serializers.CentroSaludSerializer
    entity_class = entities.CentroSalud


class AmbulanciaListCreateView(ListCreateView):
    service_factory = lambda self: CrudService(repositories.AmbulanciaRepository())
    serializer_class = serializers.AmbulanciaSerializer
    entity_class = entities.Ambulancia


class AmbulanciaDetailView(RetrieveUpdateDestroyView):
    service_factory = lambda self: CrudService(repositories.AmbulanciaRepository())
    serializer_class = serializers.AmbulanciaSerializer
    entity_class = entities.Ambulancia
