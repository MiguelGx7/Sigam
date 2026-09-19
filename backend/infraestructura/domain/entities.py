from dataclasses import dataclass
from typing import Optional


@dataclass
class CentroSalud:
    id: Optional[int]
    nombre: str
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    tipo_centro_id: Optional[int] = None


@dataclass
class Ambulancia:
    id: Optional[int]
    placa: str
    tipo_id: Optional[int] = None
    estado_id: Optional[int] = None
    centro_salud_id: Optional[int] = None
