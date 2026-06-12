from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models import TipoHabitacion
from .base import BaseRepository


class TipoHabitacionRepository(BaseRepository[TipoHabitacion]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(TipoHabitacion, session)

    async def get_by_nombre(self, nombre: str) -> TipoHabitacion | None:
        result = await self.session.execute(
            select(TipoHabitacion).where(TipoHabitacion.nombre == nombre)
        )
        return result.scalar_one_or_none()
