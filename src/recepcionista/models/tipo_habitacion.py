import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.habitacion import Habitacion


class TipoHabitacionBase(SQLModel):
    nombre: str                        = Field(max_length=50)
    descripcion: Optional[str]         = Field(default=None)
    capacidad: int
    precio_por_noche: Decimal          = Field(max_digits=10, decimal_places=2)


class TipoHabitacion(TipoHabitacionBase, table=True):
    __tablename__ = "tipos_habitaciones"
    __table_args__ = {"schema": "content"}

    id: uuid.UUID            = Field(default_factory=uuid.uuid4, primary_key=True)
    creado_en: datetime      = Field(default_factory=datetime.utcnow)
    actualizado_en: datetime = Field(default_factory=datetime.utcnow)

    habitaciones: List["Habitacion"] = Relationship(back_populates="tipo_habitacion")
