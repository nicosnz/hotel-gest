from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models import Huesped
from .base import BaseRepository


class HuespedRepository(BaseRepository[Huesped]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Huesped, session)

    async def get_by_documento(self, documento: str) -> Huesped | None:
        result = await self.session.execute(
            select(Huesped).where(Huesped.documento_identidad == documento)
        )
        return result.scalar_one_or_none()
