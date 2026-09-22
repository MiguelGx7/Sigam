from dataclasses import dataclass
from typing import Optional
import datetime
from decimal import Decimal


@dataclass
class Solicitud:
    id: Optional[int]
    usuario_id: Optional[int] = None
    estado_id: Optional[int] = None
    centro_salud_destino_id: Optional[int] = None
    ambulancia_id: Optional[int] = None
    conductor_id: Optional[int] = None
    ruta_id: Optional[int] = None
    fecha_hora: Optional[datetime.datetime] = None
    ubicacion_origen: Optional[str] = None


@dataclass
class Incidente:
    id: Optional[int]
    solicitud_id: Optional[int] = None
    tipo_id: Optional[int] = None
    prioridad_id: Optional[int] = None
    descripcion: Optional[str] = None
    observaciones: Optional[str] = None
    fecha_hora: Optional[datetime.datetime] = None
    ubicacion: Optional[str] = None
    estado_incidente: Optional[str] = None


@dataclass
class Ruta:
    id: Optional[int]
    incidente_id: Optional[int] = None
    ambulancia_id: Optional[int] = None
    conductor_id: Optional[int] = None
    centro_salud_destino_id: Optional[int] = None
    origen: Optional[str] = None
    destino: Optional[str] = None
    distancia_km: Optional[Decimal] = None
    tiempo_estimado: Optional[int] = None
    tiempo_real: Optional[int] = None
    fecha_hora_inicio: Optional[datetime.datetime] = None
    fecha_hora_fin: Optional[datetime.datetime] = None


@dataclass
class UsuarioIncidente:
    id: Optional[int]
    usuario_id: int = None
    incidente_id: int = None
