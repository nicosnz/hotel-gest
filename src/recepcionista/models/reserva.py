from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from .enums import EstadoReserva

if TYPE_CHECKING:
    from .habitacion import Habitacion
    from .reserva_huesped import ReservaHuesped
    from .pago import Pago
    from .reserva_servicio import ReservaServicio


class ReservaBase(SQLModel):
    habitacion_id: uuid.UUID               = Field(foreign_key="content.habitaciones.id")
    fecha_reserva: datetime                = Field(default_factory=datetime.utcnow)
    fecha_checkin_esperado: date
    fecha_checkout_esperado: date
    fecha_checkin_real: Optional[datetime] = Field(default=None)
    fecha_checkout_real: Optional[datetime]= Field(default=None)
    estado: EstadoReserva
    observaciones: Optional[str]           = Field(default=None)


class Reserva(ReservaBase, table=True):
    __tablename__ = "reservas"
    __table_args__ = {"schema": "content"}

    id: uuid.UUID            = Field(default_factory=uuid.uuid4, primary_key=True)
    creado_en: datetime      = Field(default_factory=datetime.utcnow)
    actualizado_en: datetime = Field(default_factory=datetime.utcnow)

    habitacion: Optional["Habitacion"]          = Relationship(back_populates="reservas")
    reserva_huespedes: list["ReservaHuesped"]   = Relationship(back_populates="reserva")
    pagos: list["Pago"]                         = Relationship(back_populates="reserva")
    reserva_servicios: list["ReservaServicio"]  = Relationship(back_populates="reserva")
