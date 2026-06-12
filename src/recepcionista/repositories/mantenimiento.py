import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models import Mantenimiento, EstadoMantenimiento
from .base import BaseRepository


class MantenimientoRepository(BaseRepository[Mantenimiento]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Mantenimiento, session)

    async def get_by_habitacion(self, habitacion_id: uuid.UUID) -> list[Mantenimiento]:
        result = await self.session.execute(
            select(Mantenimiento).where(
                Mantenimiento.habitacion_id == habitacion_id
            )
        )
        return list(result.scalars().all())

    async def get_by_estado(self, estado: EstadoMantenimiento) -> list[Mantenimiento]:
        result = await self.session.execute(
            select(Mantenimiento).where(Mantenimiento.estado == estado)
        )
        return list(result.scalars().all())

    async def get_en_proceso(self) -> list[Mantenimiento]:
        return await self.get_by_estado(EstadoMantenimiento.EN_PROCESO)
