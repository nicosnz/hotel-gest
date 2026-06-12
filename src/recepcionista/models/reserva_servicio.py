import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.reserva import Reserva
    from models.servicio import Servicio


class ReservaServicioBase(SQLModel):
    reserva_id: uuid.UUID     = Field(foreign_key="content.reservas.id", primary_key=True)
    servicio_id: uuid.UUID    = Field(foreign_key="content.servicios.id", primary_key=True)
    cantidad: int             = Field(ge=1)
    precio_unitario: Decimal  = Field(max_digits=10, decimal_places=2)
    fecha_consumo: datetime   = Field(default_factory=datetime.utcnow)


class ReservaServicio(ReservaServicioBase, table=True):
    __tablename__ = "reserva_servicios"
    __table_args__ = {"schema": "content"}

    id: uuid.UUID            = Field(default_factory=uuid.uuid4)
    creado_en: datetime      = Field(default_factory=datetime.utcnow)
    actualizado_en: datetime = Field(default_factory=datetime.utcnow)

    reserva: Optional["Reserva"]   = Relationship(back_populates="reserva_servicios")
    servicio: Optional["Servicio"] = Relationship(back_populates="reserva_servicios")
