from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime

from models import EstadoReserva
from repositories import ReservaRepository


@dataclass
class CheckinDTO:
    reserva_id: uuid.UUID
    huesped_id: uuid.UUID


@dataclass
class CheckinConfirmadoDTO:
    reserva_id: uuid.UUID
    huesped_id: uuid.UUID
    fecha_checkin_real: datetime
    estado: EstadoReserva
    mensaje: str


class CheckinService:
    def __init__(self, reserva_repo: ReservaRepository) -> None:
        self._reserva_repo = reserva_repo

    async def registrar_checkin(self, dto: CheckinDTO) -> CheckinConfirmadoDTO:
        
        reserva = await self._reserva_repo.get_by_id(dto.reserva_id)
        if not reserva:
            raise ValueError("No existe una reserva con el ID indicado.")

        
        if reserva.estado != EstadoReserva.CONFIRMADA:
            raise ValueError(
                f"La reserva no está en estado CONFIRMADA. "
                f"Estado actual: {reserva.estado.value}."
            )

        
        titular = await self._reserva_repo.get_titular(dto.reserva_id)
        if not titular or titular.huesped_id != dto.huesped_id:
            raise ValueError(
                "El huésped indicado no es el titular de esta reserva."
            )

        
        fecha_checkin_real = datetime.utcnow()
        await self._reserva_repo.update(reserva, {
            "estado": EstadoReserva.CHECKIN,
            "fecha_checkin_real": fecha_checkin_real,
        })

        return CheckinConfirmadoDTO(
            reserva_id=reserva.id,
            huesped_id=dto.huesped_id,
            fecha_checkin_real=fecha_checkin_real,
            estado=EstadoReserva.CHECKIN,
            mensaje="Check-in registrado exitosamente.",
        )