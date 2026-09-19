from common.infrastructure.django_repository import DjangoRepository

from ..domain import entities
from .. import models


class CentroSaludRepository(DjangoRepository):
    model = models.CentroSalud
    entity_class = entities.CentroSalud


class AmbulanciaRepository(DjangoRepository):
    model = models.Ambulancia
    entity_class = entities.Ambulancia
