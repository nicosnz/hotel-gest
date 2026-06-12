import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.reserva_huesped import ReservaHuesped


class HuespedBase(SQLModel):
    nombre: str                        = Field(max_length=100)
    apellido: str                      = Field(max_length=100)
    documento_identidad: str           = Field(max_length=30, unique=True)
    correo: Optional[str]              = Field(default=None, max_length=150)
    telefono: Optional[str]            = Field(default=None, max_length=20)
    fecha_registro: datetime           = Field(default_factory=datetime.utcnow)


class Huesped(HuespedBase, table=True):
    __tablename__ = "huespedes"
    __table_args__ = {"schema": "content"}

    id: uuid.UUID            = Field(default_factory=uuid.uuid4, primary_key=True)
    creado_en: datetime      = Field(default_factory=datetime.utcnow)
    actualizado_en: datetime = Field(default_factory=datetime.utcnow)

    reserva_huespedes: List["ReservaHuesped"] = Relationship(back_populates="huesped")
