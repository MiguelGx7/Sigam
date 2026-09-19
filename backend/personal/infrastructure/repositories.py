from common.infrastructure.django_repository import DjangoRepository

from ..domain import entities
from .. import models


class DatosConductorRepository(DjangoRepository):
    model = models.DatosConductor
    entity_class = entities.DatosConductor


class TurnoRepository(DjangoRepository):
    model = models.Turno
    entity_class = entities.Turno
