import uuid
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select

from models import (
    Habitacion,
    Reserva,
    ReservaHuesped,
    ReservaServicio,
    EstadoReserva,
)
from repositories.base import BaseRepository


class ReservaRepository(BaseRepository[Reserva]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Reserva, session)

    def _with_details(self):
        return (
            select(Reserva)
            .options(
                selectinload(Reserva.habitacion),
                selectinload(Reserva.reserva_huespedes).selectinload(ReservaHuesped.huesped),
                selectinload(Reserva.reserva_servicios).selectinload(ReservaServicio.servicio),
            )
        )

    async def get_all_with_details(self) -> list[Reserva]:
        result = await self.session.execute(self._with_details())
        return list(result.scalars().all())

    async def get_by_id_with_details(self, reserva_id: uuid.UUID) -> Reserva | None:
        result = await self.session.execute(
            self._with_details().where(Reserva.id == reserva_id)
        )
        return result.scalar_one_or_none()

    async def get_by_id_with_habitacion(self, reserva_id: uuid.UUID) -> Reserva | None:
        result = await self.session.execute(
            select(Reserva)
            .options(
                selectinload(Reserva.habitacion).selectinload(Habitacion.tipo_habitacion)
            )
            .where(Reserva.id == reserva_id)
        )
        return result.scalar_one_or_none()

    async def get_by_estado(self, estado: EstadoReserva) -> list[Reserva]:
        result = await self.session.execute(
            select(Reserva).where(Reserva.estado == estado.value)
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
                    [EstadoReserva.CANCELADA.value, EstadoReserva.FINALIZADA.value]
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
    
    async def get_titular(
        self, reserva_id: uuid.UUID
    ) -> ReservaHuesped | None:
        result = await self.session.execute(
            select(ReservaHuesped).where(
                ReservaHuesped.reserva_id == reserva_id,
                ReservaHuesped.es_titular == True,  
            )
        )
        return result.scalar_one_or_none()

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
            
    async def get_servicios_consumidos(
        self, reserva_id: uuid.UUID
    ) -> list[ReservaServicio]:
        result = await self.session.execute(
            select(ReservaServicio).where(
                ReservaServicio.reserva_id == reserva_id
            )
        )
        return list(result.scalars().all())

    

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
