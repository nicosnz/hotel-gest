import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.empleado import Empleado


class RolBase(SQLModel):
    nombre: str = Field(max_length=50, unique=True)


class Rol(RolBase, table=True):
    __tablename__ = "roles"
    __table_args__ = {"schema": "content"}

    id: uuid.UUID             = Field(default_factory=uuid.uuid4, primary_key=True)
    creado_en: datetime       = Field(default_factory=datetime.utcnow)
    actualizado_en: datetime  = Field(default_factory=datetime.utcnow)

    empleados: List["Empleado"] = Relationship(back_populates="rol")
