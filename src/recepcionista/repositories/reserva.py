import uuid
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models import (
    Reserva,
    ReservaHuesped,
    ReservaServicio,
    EstadoReserva,
)
from base import BaseRepository


class ReservaRepository(BaseRepository[Reserva]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Reserva, session)

    async def get_by_estado(self, estado: EstadoReserva) -> list[Reserva]:
        result = await self.session.execute(
            select(Reserva).where(Reserva.estado == estado)
        )
        return list(result.scalars().all())

    async def get_by_habitacion(self, habitacion_id: uuid.UUID) -> list[Reserva]:
        result = await self.session.execute(
            select(Reserva).where(Reserva.habitacion_id == habitacion_id)
        )
        return list(result.scalars().all())

    async def get_activas_en_rango(
        self, fecha_inicio: date, fecha_fin: date
    ) -> list[Reserva]:
        result = await self.session.execute(
            select(Reserva).where(
                Reserva.fecha_checkin_esperado < fecha_fin,
                Reserva.fecha_checkout_esperado > fecha_inicio,
                Reserva.estado.notin_(  # type: ignore[attr-defined]
                    [EstadoReserva.CANCELADA, EstadoReserva.FINALIZADA]
                ),
            )
        )
        return list(result.scalars().all())

   

    async def agregar_huesped(
        self,
        reserva: Reserva,
        huesped_id: uuid.UUID,
        es_titular: bool = False,
    ) -> ReservaHuesped:
        vinculo = ReservaHuesped(
            reserva_id=reserva.id,
            huesped_id=huesped_id,
            es_titular=es_titular,
        )
        self.session.add(vinculo)
        await self.session.commit()
        await self.session.refresh(vinculo)
        return vinculo

    async def quitar_huesped(
        self, reserva_id: uuid.UUID, huesped_id: uuid.UUID
    ) -> None:
        result = await self.session.execute(
            select(ReservaHuesped).where(
                ReservaHuesped.reserva_id == reserva_id,
                ReservaHuesped.huesped_id == huesped_id,
            )
        )
        vinculo = result.scalar_one_or_none()
        if vinculo:
            await self.session.delete(vinculo)
            await self.session.commit()

    

    async def agregar_servicio(
        self,
        reserva: Reserva,
        servicio_id: uuid.UUID,
        cantidad: int,
        precio_unitario: float,
    ) -> ReservaServicio:
        item = ReservaServicio(
            reserva_id=reserva.id,
            servicio_id=servicio_id,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
        )
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def quitar_servicio(
        self, reserva_id: uuid.UUID, servicio_id: uuid.UUID
    ) -> None:
        result = await self.session.execute(
            select(ReservaServicio).where(
                ReservaServicio.reserva_id == reserva_id,
                ReservaServicio.servicio_id == servicio_id,
            )
        )
        item = result.scalar_one_or_none()
        if item:
            await self.session.delete(item)
            await self.session.commit()
