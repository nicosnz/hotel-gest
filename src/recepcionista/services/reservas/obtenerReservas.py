from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal

from models import EstadoReserva
from repositories import ReservaRepository


@dataclass
class HuespedResumenDTO:
    id: uuid.UUID
    nombre: str
    apellido: str
    documento_identidad: str
    es_titular: bool


@dataclass
class ConsumoResumenDTO:
    servicio_nombre: str
    cantidad: int
    precio_unitario: Decimal
    subtotal: Decimal
    fecha_consumo: datetime


@dataclass
class ReservaResumenDTO:
    id: uuid.UUID
    habitacion_numero: str
    estado: EstadoReserva
    fecha_checkin_esperado: date
    fecha_checkout_esperado: date
    fecha_checkin_real: datetime | None
    fecha_checkout_real: datetime | None
    observaciones: str | None
    huespedes: list[HuespedResumenDTO] = field(default_factory=list)
    consumos: list[ConsumoResumenDTO] = field(default_factory=list)


class ReservaQueryService:
    def __init__(self, reserva_repo: ReservaRepository) -> None:
        self._reserva_repo = reserva_repo

    async def listar_reservas(self) -> list[ReservaResumenDTO]:
        reservas = await self._reserva_repo.get_all_with_details()
        return [self._to_dto(r) for r in reservas]

    async def obtener_reserva(self, reserva_id: uuid.UUID) -> ReservaResumenDTO:
        reserva = await self._reserva_repo.get_by_id_with_details(reserva_id)
        if not reserva:
            raise ValueError("No existe una reserva con el ID indicado.")
        return self._to_dto(reserva)

    def _to_dto(self, reserva) -> ReservaResumenDTO:
        huespedes = [
            HuespedResumenDTO(
                id=rh.huesped.id,
                nombre=rh.huesped.nombre,
                apellido=rh.huesped.apellido,
                documento_identidad=rh.huesped.documento_identidad,
                es_titular=rh.es_titular,
            )
            for rh in reserva.reserva_huespedes
            if rh.huesped is not None
        ]

        consumos = [
            ConsumoResumenDTO(
                servicio_nombre=rs.servicio.nombre,
                cantidad=rs.cantidad,
                precio_unitario=rs.precio_unitario,
                subtotal=rs.precio_unitario * rs.cantidad,
                fecha_consumo=rs.fecha_consumo,
            )
            for rs in reserva.reserva_servicios
            if rs.servicio is not None
        ]

        return ReservaResumenDTO(
            id=reserva.id,
            habitacion_numero=reserva.habitacion.numero if reserva.habitacion else str(reserva.habitacion_id),
            estado=reserva.estado,
            fecha_checkin_esperado=reserva.fecha_checkin_esperado,
            fecha_checkout_esperado=reserva.fecha_checkout_esperado,
            fecha_checkin_real=reserva.fecha_checkin_real,
            fecha_checkout_real=reserva.fecha_checkout_real,
            observaciones=reserva.observaciones,
            huespedes=huespedes,
            consumos=consumos,
        )
