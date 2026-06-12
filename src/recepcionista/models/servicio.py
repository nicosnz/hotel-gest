import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.reserva_servicio import ReservaServicio


class ServicioBase(SQLModel):
    nombre: str                = Field(max_length=100)
    descripcion: Optional[str] = Field(default=None)
    precio: Decimal            = Field(max_digits=10, decimal_places=2)
    activo: bool               = Field(default=True)


class Servicio(ServicioBase, table=True):
    __tablename__ = "servicios"
    __table_args__ = {"schema": "content"}

    id: uuid.UUID            = Field(default_factory=uuid.uuid4, primary_key=True)
    creado_en: datetime      = Field(default_factory=datetime.utcnow)
    actualizado_en: datetime = Field(default_factory=datetime.utcnow)

    reserva_servicios: List["ReservaServicio"] = Relationship(back_populates="servicio")
