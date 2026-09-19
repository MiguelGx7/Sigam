from dataclasses import dataclass
from typing import Optional


@dataclass
class Prioridad:
    id: Optional[int]
    nombre: str
    nivel: Optional[str] = None
    tiempo_respuesta_max: Optional[int] = None


@dataclass
class EstadoSolicitud:
    """Catalogo de estados de una solicitud (tabla 'estado')."""
    id: Optional[int]
    nombre: str
    descripcion: Optional[str] = None


@dataclass
class EstadoTipoIncidente:
    """Catalogo de estados de un tipo de incidente (tabla 'estados')."""
    id: Optional[int]
    nombre: str
    descripcion: Optional[str] = None


@dataclass
class TipoCentro:
    id: Optional[int]
    nombre: str


@dataclass
class TipoAmbulancia:
    id: Optional[int]
    nombre: str
    descripcion: Optional[str] = None


@dataclass
class EstadoAmbulancia:
    id: Optional[int]
    nombre: str
    descripcion: Optional[str] = None


@dataclass
class TipoIncidente:
    id: Optional[int]
    nombre: str
    estado_id: int
    descripcion: Optional[str] = None
