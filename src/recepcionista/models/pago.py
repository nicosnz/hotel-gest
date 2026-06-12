import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from models.enums import ConceptoPago, EstadoPago, MetodoPago

if TYPE_CHECKING:
    from models.reserva import Reserva


class PagoBase(SQLModel):
    reserva_id: uuid.UUID  = Field(foreign_key="content.reservas.id")
    monto: Decimal         = Field(max_digits=10, decimal_places=2)
    concepto: ConceptoPago
    metodo_pago: MetodoPago
    fecha_pago: datetime   = Field(default_factory=datetime.utcnow)
    estado: EstadoPago


class Pago(PagoBase, table=True):
    __tablename__ = "pagos"
    __table_args__ = {"schema": "content"}

    id: uuid.UUID            = Field(default_factory=uuid.uuid4, primary_key=True)
    creado_en: datetime      = Field(default_factory=datetime.utcnow)
    actualizado_en: datetime = Field(default_factory=datetime.utcnow)

    reserva: Optional["Reserva"] = Relationship(back_populates="pagos")
