from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from models import EstadoReserva
from repositories import ReservaRepository, ServicioRepository


@dataclass
class RegistrarConsumoDTO:
    reserva_id: uuid.UUID
    servicio_id: uuid.UUID
    cantidad: int


@dataclass
class ConsumoRegistradoDTO:
    reserva_id: uuid.UUID
    servicio_id: uuid.UUID
    servicio_nombre: str
    cantidad: int
    precio_unitario: Decimal
    subtotal: Decimal
    fecha_consumo: datetime
    saldo_acumulado: Decimal
    mensaje: str


class ConsumoService:
    def __init__(
        self,
        reserva_repo: ReservaRepository,
        servicio_repo: ServicioRepository,
    ) -> None:
        self._reserva_repo = reserva_repo
        self._servicio_repo = servicio_repo

    async def registrar_consumo(
        self, dto: RegistrarConsumoDTO
    ) -> ConsumoRegistradoDTO:
        # ------------------------------------------------------------------
        # 1. Validar cantidad
        # ------------------------------------------------------------------
        if dto.cantidad < 1:
            raise ValueError("La cantidad debe ser mayor a cero.")

        # ------------------------------------------------------------------
        # 2. Verificar que la reserva existe y está en CHECKIN
        # ------------------------------------------------------------------
        reserva = await self._reserva_repo.get_by_id(dto.reserva_id)
        if not reserva:
            raise ValueError("No existe una reserva con el ID indicado.")

        if reserva.estado != EstadoReserva.CHECKIN:
            raise ValueError(
                "No existe una estadía activa para esta reserva. "
                f"Estado actual: {reserva.estado.value}."
            )

        # ------------------------------------------------------------------
        # 3. Verificar que el servicio existe y está activo
        # ------------------------------------------------------------------
        servicio = await self._servicio_repo.get_by_id(dto.servicio_id)
        if not servicio:
            raise ValueError("El servicio indicado no existe.")

        if not servicio.activo:
            raise ValueError(
                f"El servicio '{servicio.nombre}' no está disponible actualmente."
            )

        # ------------------------------------------------------------------
        # 4. Registrar el consumo con el precio vigente del servicio
        # ------------------------------------------------------------------
        consumo = await self._reserva_repo.agregar_servicio(
            reserva=reserva,
            servicio_id=servicio.id,
            cantidad=dto.cantidad,
            precio_unitario=servicio.precio,
        )

        # ------------------------------------------------------------------
        # 5. Calcular saldo acumulado de todos los consumos de la reserva
        # ------------------------------------------------------------------
        consumos = await self._reserva_repo.get_servicios_consumidos(dto.reserva_id)
        saldo_acumulado: Decimal = sum(
            c.precio_unitario * c.cantidad for c in consumos
        )

        subtotal = servicio.precio * dto.cantidad

        return ConsumoRegistradoDTO(
            reserva_id=reserva.id,
            servicio_id=servicio.id,
            servicio_nombre=servicio.nombre,
            cantidad=dto.cantidad,
            precio_unitario=servicio.precio,
            subtotal=subtotal,
            fecha_consumo=consumo.fecha_consumo,
            saldo_acumulado=saldo_acumulado,
            mensaje="Consumo registrado exitosamente.",
        )