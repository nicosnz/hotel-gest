from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models import Rol
from repositories.base import BaseRepository


class RolRepository(BaseRepository[Rol]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Rol, session)

    async def get_by_nombre(self, nombre: str) -> Rol | None:
        result = await self.session.execute(
            select(Rol).where(Rol.nombre == nombre)
        )
        return result.scalar_one_or_none()
