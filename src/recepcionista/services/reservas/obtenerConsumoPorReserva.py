from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from models import EstadoReserva
from repositories import ReservaRepository, ServicioRepository


@dataclass
class ConsumoDetalleDTO:
    servicio_id: uuid.UUID
    servicio_nombre: str
    cantidad: int
    precio_unitario: Decimal
    subtotal: Decimal
    fecha_consumo: datetime


@dataclass
class ConsumosReservaDTO:
    reserva_id: uuid.UUID
    estado_reserva: EstadoReserva
    consumos: list[ConsumoDetalleDTO]
    total_acumulado: Decimal
    mensaje: str


class ConsultaConsumoService:
    def __init__(
        self,
        reserva_repo: ReservaRepository,
        servicio_repo: ServicioRepository,
    ) -> None:
        self._reserva_repo = reserva_repo
        self._servicio_repo = servicio_repo

    async def consultar_consumos(self, reserva_id: uuid.UUID) -> ConsumosReservaDTO:
        # ------------------------------------------------------------------
        # 1. Verificar que la reserva existe
        # ------------------------------------------------------------------
        reserva = await self._reserva_repo.get_by_id(reserva_id)
        if not reserva:
            raise ValueError("No existe una reserva con el ID indicado.")

        # ------------------------------------------------------------------
        # 2. Traer consumos registrados
        # ------------------------------------------------------------------
        consumos_raw = await self._reserva_repo.get_servicios_consumidos(reserva_id)

        if not consumos_raw:
            return ConsumosReservaDTO(
                reserva_id=reserva.id,
                estado_reserva=reserva.estado,
                consumos=[],
                total_acumulado=Decimal("0.00"),
                mensaje="No existen consumos registrados para esta reserva.",
            )

        # ------------------------------------------------------------------
        # 3. Enriquecer cada consumo con el nombre del servicio
        # ------------------------------------------------------------------
        detalle: list[ConsumoDetalleDTO] = []
        for consumo in consumos_raw:
            servicio = await self._servicio_repo.get_by_id(consumo.servicio_id)
            detalle.append(
                ConsumoDetalleDTO(
                    servicio_id=consumo.servicio_id,
                    servicio_nombre=servicio.nombre if servicio else "Servicio eliminado",
                    cantidad=consumo.cantidad,
                    precio_unitario=consumo.precio_unitario,
                    subtotal=consumo.precio_unitario * consumo.cantidad,
                    fecha_consumo=consumo.fecha_consumo,
                )
            )

        total_acumulado: Decimal = sum(d.subtotal for d in detalle)

        return ConsumosReservaDTO(
            reserva_id=reserva.id,
            estado_reserva=reserva.estado,
            consumos=detalle,
            total_acumulado=total_acumulado,
            mensaje="Consumos obtenidos exitosamente.",
        )