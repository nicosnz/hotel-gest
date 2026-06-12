from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models import Empleado
from .base import BaseRepository


class EmpleadoRepository(BaseRepository[Empleado]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Empleado, session)

    async def get_by_correo(self, correo: str) -> Empleado | None:
        result = await self.session.execute(
            select(Empleado).where(Empleado.correo == correo)
        )
        return result.scalar_one_or_none()

    async def get_activos(self) -> list[Empleado]:
        result = await self.session.execute(
            select(Empleado).where(Empleado.activo == True)  # noqa: E712
        )
        return list(result.scalars().all())
