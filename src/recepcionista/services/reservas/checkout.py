from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from models import (
    EstadoHabitacion,
    EstadoPago,
    EstadoReserva,
    ConceptoPago,
    MetodoPago,
    Pago,
    Reserva,
)
from repositories import HabitacionRepository, PagoRepository, ReservaRepository


@dataclass
class CheckoutDTO:
    reserva_id: uuid.UUID
    monto_pago: Decimal
    metodo_pago: MetodoPago


@dataclass
class CheckoutConfirmadoDTO:
    reserva_id: uuid.UUID
    habitacion_id: uuid.UUID
    costo_hospedaje: Decimal
    total_consumos: Decimal
    total_final: Decimal
    adelanto_pagado: Decimal
    saldo_pagado: Decimal
    fecha_checkout_real: datetime
    mensaje: str


class CheckoutService:
    def __init__(
        self,
        reserva_repo: ReservaRepository,
        habitacion_repo: HabitacionRepository,
        pago_repo: PagoRepository,
    ) -> None:
        self._reserva_repo = reserva_repo
        self._habitacion_repo = habitacion_repo
        self._pago_repo = pago_repo

    # ------------------------------------------------------------------
    # Método principal — solo orquesta
    # ------------------------------------------------------------------

    async def realizar_checkout(self, dto: CheckoutDTO) -> CheckoutConfirmadoDTO:
        reserva = await self._obtener_reserva_en_checkin(dto.reserva_id)
        habitacion = reserva.habitacion

        costo_hospedaje = await self._calcular_costo_hospedaje(reserva)
        total_consumos = await self._calcular_total_consumos(reserva.id)
        total_final = costo_hospedaje + total_consumos

        adelanto_pagado = await self._calcular_adelanto_pagado(reserva.id)
        saldo_pendiente = total_final - adelanto_pagado

        self._validar_pago(dto.monto_pago, saldo_pendiente)

        await self._registrar_pago_hospedaje(reserva.id, dto.monto_pago, dto.metodo_pago)

        fecha_checkout_real = datetime.utcnow()
        await self._finalizar_reserva(reserva, fecha_checkout_real)
        await self._liberar_habitacion(habitacion)

        return CheckoutConfirmadoDTO(
            reserva_id=reserva.id,
            habitacion_id=habitacion.id,
            costo_hospedaje=costo_hospedaje,
            total_consumos=total_consumos,
            total_final=total_final,
            adelanto_pagado=adelanto_pagado,
            saldo_pagado=dto.monto_pago,
            fecha_checkout_real=fecha_checkout_real,
            mensaje="Check-out realizado exitosamente. Habitación liberada.",
        )

    # ------------------------------------------------------------------
    # Métodos privados — cada uno hace una sola cosa
    # ------------------------------------------------------------------

    async def _obtener_reserva_en_checkin(self, reserva_id: uuid.UUID) -> Reserva:
        reserva = await self._reserva_repo.get_by_id_with_habitacion(reserva_id)
        if not reserva:
            raise ValueError("No existe una reserva con el ID indicado.")
        if reserva.estado != EstadoReserva.CHECKIN:
            raise ValueError(
                "La reserva no tiene una estadía activa. "
                f"Estado actual: {reserva.estado}."
            )
        return reserva

    async def _calcular_costo_hospedaje(self, reserva: Reserva) -> Decimal:
        noches = (reserva.fecha_checkout_esperado - reserva.fecha_checkin_esperado).days
        return reserva.habitacion.tipo_habitacion.precio_por_noche * noches

    async def _calcular_total_consumos(self, reserva_id: uuid.UUID) -> Decimal:
        consumos = await self._reserva_repo.get_servicios_consumidos(reserva_id)
        return sum(
            (c.precio_unitario * c.cantidad for c in consumos),
            Decimal("0.00"),
        )

    async def _calcular_adelanto_pagado(self, reserva_id: uuid.UUID) -> Decimal:
        pagos = await self._pago_repo.get_by_reserva(reserva_id)
        return sum(
            (p.monto for p in pagos if p.estado == EstadoPago.PAGADO),
            Decimal("0.00"),
        )

    def _validar_pago(self, monto_pago: Decimal, saldo_pendiente: Decimal) -> None:
        if monto_pago > saldo_pendiente:
            raise ValueError(
                f"El monto ingresado ({monto_pago:.2f}) supera el saldo pendiente "
                f"({saldo_pendiente:.2f})."
            )
        if monto_pago < saldo_pendiente:
            raise ValueError(
                f"El monto ingresado ({monto_pago:.2f}) no cubre el saldo pendiente "
                f"({saldo_pendiente:.2f})."
            )

    async def _registrar_pago_hospedaje(
        self,
        reserva_id: uuid.UUID,
        monto: Decimal,
        metodo_pago: MetodoPago,
    ) -> None:
        await self._pago_repo.create(
            Pago(
                reserva_id=reserva_id,
                monto=monto,
                concepto=ConceptoPago.HOSPEDAJE.value,
                metodo_pago=metodo_pago.value if hasattr(metodo_pago, 'value') else metodo_pago,
                estado=EstadoPago.PAGADO.value,
            )
        )

    async def _finalizar_reserva(
        self, reserva: Reserva, fecha_checkout_real: datetime
    ) -> None:
        await self._reserva_repo.update(reserva, {
            "estado": EstadoReserva.FINALIZADA.value,
            "fecha_checkout_real": fecha_checkout_real,
        })

    async def _liberar_habitacion(self, habitacion) -> None:
        if habitacion.estado == EstadoHabitacion.DISPONIBLE.value:
            return
        await self._habitacion_repo.update(habitacion, {
            "estado": EstadoHabitacion.DISPONIBLE.value,
        })