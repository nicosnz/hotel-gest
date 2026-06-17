from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID

from models import EstadoHabitacion, Habitacion
from repositories import HabitacionRepository, ReservaRepository


@dataclass
class HabitacionDisponibleDTO:
    id: UUID
    numero: str
    piso: int
    tipo: str
    capacidad: int
    precio_por_noche: Decimal


@dataclass
class DisponibilidadResultadoDTO:
    fecha_checkin: date
    fecha_checkout: date
    noches: int
    habitaciones: list[HabitacionDisponibleDTO]
    mensaje: str


class HabitacionService:
    def __init__(
        self,
        habitacion_repo: HabitacionRepository,
        reserva_repo: ReservaRepository,
    ) -> None:
        self._habitacion_repo = habitacion_repo
        self._reserva_repo = reserva_repo

    async def consultar_disponibilidad(
        self,
        fecha_checkin: date,
        fecha_checkout: date,
    ) -> DisponibilidadResultadoDTO:
        # ------------------------------------------------------------------
        # 1. Validar fechas
        # ------------------------------------------------------------------
        if fecha_checkout <= fecha_checkin:
            raise ValueError(
                "La fecha de check-out debe ser posterior a la fecha de check-in."
            )

        # ------------------------------------------------------------------
        # 2. Obtener habitaciones en estado DISPONIBLE
        # ------------------------------------------------------------------
        habitaciones_disponibles = await self._habitacion_repo.get_disponibles()

        # ------------------------------------------------------------------
        # 3. Obtener reservas activas en el rango solicitado
        # ------------------------------------------------------------------
        reservas_en_rango = await self._reserva_repo.get_activas_en_rango(
            fecha_checkin,
            fecha_checkout,
        )

        # IDs de habitaciones ocupadas en ese rango
        ids_ocupadas = {r.habitacion_id for r in reservas_en_rango}

        # ------------------------------------------------------------------
        # 4. Filtrar habitaciones sin conflicto
        # ------------------------------------------------------------------
        libres = [
            h for h in habitaciones_disponibles
            if h.id not in ids_ocupadas
        ]

        noches = (fecha_checkout - fecha_checkin).days

        return DisponibilidadResultadoDTO(
            fecha_checkin=fecha_checkin,
            fecha_checkout=fecha_checkout,
            noches=noches,
            habitaciones=[
                HabitacionDisponibleDTO(
                    id=h.id,
                    numero=h.numero,
                    piso=h.piso,
                    tipo=h.tipo_habitacion.nombre,
                    capacidad=h.tipo_habitacion.capacidad,
                    precio_por_noche=h.tipo_habitacion.precio_por_noche,
                )
                for h in libres
            ],
            mensaje=(
                "Se encontraron habitaciones disponibles para el período solicitado."
                if libres
                else "No existen habitaciones disponibles para el período solicitado."
            ),
        )