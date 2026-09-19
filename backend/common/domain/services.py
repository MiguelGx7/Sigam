from typing import Generic, Iterable, Optional

from .ports import Entidad, Repository


class CrudService(Generic[Entidad]):
    """Caso de uso CRUD generico: orquesta un Repository (puerto) sin saber nada de Django."""

    def __init__(self, repo: Repository[Entidad]):
        self.repo = repo

    def listar(self) -> Iterable[Entidad]:
        return self.repo.listar()

    def obtener(self, id: int) -> Optional[Entidad]:
        return self.repo.obtener(id)

    def crear(self, entidad: Entidad) -> Entidad:
        return self.repo.crear(entidad)

    def actualizar(self, id: int, entidad: Entidad) -> Entidad:
        return self.repo.actualizar(id, entidad)

    def eliminar(self, id: int) -> None:
        self.repo.eliminar(id)
