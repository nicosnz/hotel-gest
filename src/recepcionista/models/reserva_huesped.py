import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.reserva import Reserva
    from models.huesped import Huesped


class ReservaHuespedBase(SQLModel):
    reserva_id: uuid.UUID = Field(foreign_key="content.reservas.id", primary_key=True)
    huesped_id: uuid.UUID = Field(foreign_key="content.huespedes.id", primary_key=True)
    es_titular: bool      = Field(default=False)


class ReservaHuesped(ReservaHuespedBase, table=True):
    __tablename__ = "reserva_huespedes"
    __table_args__ = {"schema": "content"}

    id: uuid.UUID            = Field(default_factory=uuid.uuid4)
    creado_en: datetime      = Field(default_factory=datetime.utcnow)
    actualizado_en: datetime = Field(default_factory=datetime.utcnow)

    reserva: Optional["Reserva"]  = Relationship(back_populates="reserva_huespedes")
    huesped: Optional["Huesped"]  = Relationship(back_populates="reserva_huespedes")
