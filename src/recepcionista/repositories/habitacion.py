from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models import Habitacion, EstadoHabitacion
from repositories.base import BaseRepository


class HabitacionRepository(BaseRepository[Habitacion]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Habitacion, session)

    async def get_by_numero(self, numero: str) -> Habitacion | None:
        result = await self.session.execute(
            select(Habitacion).where(Habitacion.numero == numero)
        )
        return result.scalar_one_or_none()

    async def get_by_estado(self, estado: EstadoHabitacion) -> list[Habitacion]:
        result = await self.session.execute(
            select(Habitacion).where(Habitacion.estado == estado)
        )
        return list(result.scalars().all())

    async def get_disponibles(self) -> list[Habitacion]:
        return await self.get_by_estado(EstadoHabitacion.DISPONIBLE)
