from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from .enums import EstadoHabitacion

if TYPE_CHECKING:
    from .tipo_habitacion import TipoHabitacion
    from .reserva import Reserva
    from .mantenimiento import Mantenimiento


class HabitacionBase(SQLModel):
    numero: str                              = Field(max_length=10, unique=True)
    piso: int
    tipo_habitacion_id: uuid.UUID            = Field(foreign_key="content.tipos_habitaciones.id")
    estado: EstadoHabitacion


class Habitacion(HabitacionBase, table=True):
    __tablename__ = "habitaciones"
    __table_args__ = {"schema": "content"}

    id: uuid.UUID            = Field(default_factory=uuid.uuid4, primary_key=True)
    creado_en: datetime      = Field(default_factory=datetime.utcnow)
    actualizado_en: datetime = Field(default_factory=datetime.utcnow)

    tipo_habitacion: Optional["TipoHabitacion"]  = Relationship(back_populates="habitaciones")
    reservas: list["Reserva"]                    = Relationship(back_populates="habitacion")
    mantenimientos: list["Mantenimiento"]        = Relationship(back_populates="habitacion")
