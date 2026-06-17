import uuid
from datetime import datetime
from sqlmodel import Field, SQLModel


class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"

    id: uuid.UUID         = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str         = Field(max_length=50, unique=True, index=True)
    password_hash: str    = Field(max_length=255)
    nombre: str           = Field(max_length=100)
    apellido: str         = Field(max_length=100)
    activo: bool          = Field(default=True)
    creado_en: datetime   = Field(default_factory=datetime.utcnow)
