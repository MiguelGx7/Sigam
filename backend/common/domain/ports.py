from abc import ABC, abstractmethod
from typing import Generic, Iterable, Optional, TypeVar

Entidad = TypeVar('Entidad')


class Repository(ABC, Generic[Entidad]):
    """Puerto de persistencia. El dominio depende de esta interfaz, nunca del ORM de Django."""

    @abstractmethod
    def listar(self) -> Iterable[Entidad]: ...

    @abstractmethod
    def obtener(self, id: int) -> Optional[Entidad]: ...

    @abstractmethod
    def crear(self, entidad: Entidad) -> Entidad: ...

    @abstractmethod
    def actualizar(self, id: int, entidad: Entidad) -> Entidad: ...

    @abstractmethod
    def eliminar(self, id: int) -> None: ...
