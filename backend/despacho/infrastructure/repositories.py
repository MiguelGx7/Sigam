from common.infrastructure.django_repository import DjangoRepository

from ..domain import entities
from .. import models


class SolicitudRepository(DjangoRepository):
    model = models.Solicitud
    entity_class = entities.Solicitud


class IncidenteRepository(DjangoRepository):
    model = models.Incidente
    entity_class = entities.Incidente


class RutaRepository(DjangoRepository):
    model = models.Ruta
    entity_class = entities.Ruta


class UsuarioIncidenteRepository(DjangoRepository):
    model = models.UsuarioIncidente
    entity_class = entities.UsuarioIncidente
