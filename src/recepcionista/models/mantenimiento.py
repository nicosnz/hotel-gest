import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from models.enums import EstadoMantenimiento

if TYPE_CHECKING:
    from models.habitacion import Habitacion
    from models.empleado import Empleado


class MantenimientoBase(SQLModel):
    habitacion_id: uuid.UUID          = Field(foreign_key="content.habitaciones.id")
    empleado_id: Optional[uuid.UUID]  = Field(default=None, foreign_key="content.empleados.id")
    fecha_inicio: datetime
    fecha_fin: Optional[datetime]     = Field(default=None)
    descripcion: str
    estado: EstadoMantenimiento


class Mantenimiento(MantenimientoBase, table=True):
    __tablename__ = "mantenimientos"
    __table_args__ = {"schema": "content"}

    id: uuid.UUID            = Field(default_factory=uuid.uuid4, primary_key=True)
    creado_en: datetime      = Field(default_factory=datetime.utcnow)
    actualizado_en: datetime = Field(default_factory=datetime.utcnow)

    habitacion: Optional["Habitacion"] = Relationship(back_populates="mantenimientos")
    empleado: Optional["Empleado"]     = Relationship(back_populates="mantenimientos")
