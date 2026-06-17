from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models import Servicio
from repositories.base import BaseRepository


class ServicioRepository(BaseRepository[Servicio]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Servicio, session)

    async def get_activos(self) -> list[Servicio]:
        result = await self.session.execute(
            select(Servicio).where(Servicio.activo == True)  # noqa: E712
        )
        return list(result.scalars().all())
