import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models import Pago, EstadoPago
from repositories.base import BaseRepository


class PagoRepository(BaseRepository[Pago]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Pago, session)

    async def get_by_reserva(self, reserva_id: uuid.UUID) -> list[Pago]:
        result = await self.session.execute(
            select(Pago).where(Pago.reserva_id == reserva_id)
        )
        return list(result.scalars().all())

    async def get_by_estado(self, estado: EstadoPago) -> list[Pago]:
        result = await self.session.execute(
            select(Pago).where(Pago.estado == estado)
        )
        return list(result.scalars().all())
