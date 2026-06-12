import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel

from models.enums import EstadoReserva

if TYPE_CHECKING:
    from models.habitacion import Habitacion
    from models.reserva_huesped import ReservaHuesped
    from models.pago import Pago
    from models.reserva_servicio import ReservaServicio


class ReservaBase(SQLModel):
    habitacion_id: uuid.UUID               = Field(foreign_key="content.habitaciones.id")
    fecha_reserva: datetime                = Field(default_factory=datetime.utcnow)
    fecha_checkin_esperado: date
    fecha_checkout_esperado: date
    fecha_checkin_real: Optional[datetime] = Field(default=None)
    fecha_checkout_real: Optional[datetime]= Field(default=None)
    estado: EstadoReserva = Field(sa_column=Column(String, nullable=False))
    observaciones: Optional[str]           = Field(default=None)


class Reserva(ReservaBase, table=True):
    __tablename__ = "reservas"
    __table_args__ = {"schema": "content"}

    id: uuid.UUID            = Field(default_factory=uuid.uuid4, primary_key=True)
    creado_en: datetime      = Field(default_factory=datetime.utcnow)
    actualizado_en: datetime = Field(default_factory=datetime.utcnow)

    habitacion: Optional["Habitacion"]          = Relationship(back_populates="reservas")
    reserva_huespedes: List["ReservaHuesped"]   = Relationship(back_populates="reserva")
    pagos: List["Pago"]                         = Relationship(back_populates="reserva")
    reserva_servicios: List["ReservaServicio"]  = Relationship(back_populates="reserva")
