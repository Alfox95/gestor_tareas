from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional


@dataclass
class Usuario:
    id: int
    nombre: str


# Días que se usan cuando la tarea no tiene fecha límite (para no olvidarla en la lista)
DIAS_POR_DEFECTO = 60


@dataclass
class Tarea:
    id: int
    descripcion: str
    prioridad: int = 3  # 1 = muy baja, 5 = urgente
    fecha_max: Optional[date] = None
    fecha_creado: datetime = field(default_factory=datetime.now)
    fecha_realizada: Optional[datetime] = None
    creador: Optional[Usuario] = None
    completador: Optional[Usuario] = None
    tipo_tarea: Optional[str] = None
    completo: bool = False

    def dias_restantes(self) -> Optional[int]:
        if self.fecha_max is None:
            return None
        hoy = date.today()
        return (self.fecha_max - hoy).days

    def dias_restantes_para_ordenar(self) -> int:
        """Para ordenar y mostrar: sin fecha límite = DIAS_POR_DEFECTO (60)."""
        d = self.dias_restantes()
        return DIAS_POR_DEFECTO if d is None else d

    def toggle_completo(self) -> None:
        self.completo = not self.completo

    def editar_prioridad(self, nueva_prioridad: int) -> None:
        self.prioridad = nueva_prioridad

    def editar_fecha_max(self, nueva_fecha_max: date) -> None:
        self.fecha_max = nueva_fecha_max

    def editar_tipo(self, nuevo_tipo: str) -> None:
        self.tipo_tarea = nuevo_tipo

