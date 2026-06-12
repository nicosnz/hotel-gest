from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .rol import Rol
    from .mantenimiento import Mantenimiento


class EmpleadoBase(SQLModel):
    rol_id: uuid.UUID             = Field(foreign_key="content.roles.id")
    nombre: str                   = Field(max_length=100)
    apellido: str                 = Field(max_length=100)
    correo: Optional[str]         = Field(default=None, max_length=150, unique=True)
    telefono: Optional[str]       = Field(default=None, max_length=20, unique=True)
    fecha_contratacion: date
    activo: bool                  = Field(default=True)


class Empleado(EmpleadoBase, table=True):
    __tablename__ = "empleados"
    __table_args__ = {"schema": "content"}

    id: uuid.UUID            = Field(default_factory=uuid.uuid4, primary_key=True)
    creado_en: datetime      = Field(default_factory=datetime.utcnow)
    actualizado_en: datetime = Field(default_factory=datetime.utcnow)

    rol: Optional["Rol"]                  = Relationship(back_populates="empleados")
    mantenimientos: list["Mantenimiento"] = Relationship(back_populates="empleado")
