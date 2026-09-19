from common.infrastructure.django_repository import DjangoRepository

from ..domain import entities
from .. import models


class PrioridadRepository(DjangoRepository):
    model = models.Prioridad
    entity_class = entities.Prioridad


class EstadoSolicitudRepository(DjangoRepository):
    model = models.EstadoSolicitud
    entity_class = entities.EstadoSolicitud


class EstadoTipoIncidenteRepository(DjangoRepository):
    model = models.EstadoTipoIncidente
    entity_class = entities.EstadoTipoIncidente


class TipoCentroRepository(DjangoRepository):
    model = models.TipoCentro
    entity_class = entities.TipoCentro


class TipoAmbulanciaRepository(DjangoRepository):
    model = models.TipoAmbulancia
    entity_class = entities.TipoAmbulancia


class EstadoAmbulanciaRepository(DjangoRepository):
    model = models.EstadoAmbulancia
    entity_class = entities.EstadoAmbulancia


class TipoIncidenteRepository(DjangoRepository):
    model = models.TipoIncidente
    entity_class = entities.TipoIncidente
