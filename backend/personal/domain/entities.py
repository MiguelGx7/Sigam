from dataclasses import dataclass
from typing import Optional
import datetime


@dataclass
class DatosConductor:
    id: Optional[int]
    usuario_id: Optional[int] = None
    licencia: Optional[str] = None
    categoria_licencia: Optional[str] = None
    fecha_vencimiento: Optional[datetime.date] = None
    centro_salud_id: Optional[int] = None
    estado: Optional[str] = None


@dataclass
class Turno:
    id: Optional[int]
    conductor_id: Optional[int] = None
    ambulancia_id: Optional[int] = None
    fecha: Optional[datetime.date] = None
    hora_inicio: Optional[datetime.time] = None
    hora_fin: Optional[datetime.time] = None
    estado_turno: Optional[str] = None
