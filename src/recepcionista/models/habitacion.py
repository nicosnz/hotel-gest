import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel

from models.enums import EstadoHabitacion

if TYPE_CHECKING:
    from models.tipo_habitacion import TipoHabitacion
    from models.reserva import Reserva
    from models.mantenimiento import Mantenimiento


class HabitacionBase(SQLModel):
    numero: str                              = Field(max_length=10, unique=True)
    piso: int
    tipo_habitacion_id: uuid.UUID            = Field(foreign_key="content.tipos_habitaciones.id")
    estado: EstadoHabitacion = Field(sa_column=Column(String, nullable=False))


class Habitacion(HabitacionBase, table=True):
    __tablename__ = "habitaciones"
    __table_args__ = {"schema": "content"}

    id: uuid.UUID            = Field(default_factory=uuid.uuid4, primary_key=True)
    creado_en: datetime      = Field(default_factory=datetime.utcnow)
    actualizado_en: datetime = Field(default_factory=datetime.utcnow)

    tipo_habitacion: Optional["TipoHabitacion"]  = Relationship(back_populates="habitaciones")
    reservas: List["Reserva"]                    = Relationship(back_populates="habitacion")
    mantenimientos: List["Mantenimiento"]        = Relationship(back_populates="habitacion")
