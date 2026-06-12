from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal

from models import (
    ConceptoPago,
    EstadoPago,
    EstadoReserva,
    MetodoPago,
    Pago,
    Reserva,
)
from repositories import HabitacionRepository, PagoRepository, ReservaRepository


@dataclass
class CrearReservaDTO:
    habitacion_id: uuid.UUID
    fecha_checkin_esperado: date
    fecha_checkout_esperado: date
    huesped_titular_id: uuid.UUID
    monto_adelanto: Decimal
    metodo_pago: MetodoPago
    huespedes_adicionales: list[uuid.UUID] = field(default_factory=list)


@dataclass
class ReservaConfirmadaDTO:
    reserva_id: uuid.UUID
    estado: EstadoReserva
    total_estimado: Decimal
    pago_id: uuid.UUID
    mensaje: str


class ReservaService:
    def __init__(
        self,
        reserva_repo: ReservaRepository,
        habitacion_repo: HabitacionRepository,
        pago_repo: PagoRepository,
    ) -> None:
        self._reserva_repo = reserva_repo
        self._habitacion_repo = habitacion_repo
        self._pago_repo = pago_repo

    async def crear_reserva(self, dto: CrearReservaDTO) -> ReservaConfirmadaDTO:
        # ------------------------------------------------------------------
        # 1. Validar fechas
        # ------------------------------------------------------------------
        if dto.fecha_checkout_esperado <= dto.fecha_checkin_esperado:
            raise ValueError(
                "La fecha de check-out debe ser posterior a la fecha de check-in."
            )

        # ------------------------------------------------------------------
        # 2. Verificar que la habitación existe
        # ------------------------------------------------------------------
        habitacion = await self._habitacion_repo.get_by_id(dto.habitacion_id)
        if not habitacion:
            raise ValueError("La habitación indicada no existe.")

        # ------------------------------------------------------------------
        # 3. Verificar disponibilidad en el rango de fechas
        # ------------------------------------------------------------------
        conflictos = await self._reserva_repo.get_activas_en_rango(
            dto.fecha_checkin_esperado,
            dto.fecha_checkout_esperado,
        )
        ocupada = any(r.habitacion_id == dto.habitacion_id for r in conflictos)
        if ocupada:
            raise ValueError(
                "La habitación no está disponible para las fechas solicitadas."
            )

        # ------------------------------------------------------------------
        # 4. Calcular total estimado
        # ------------------------------------------------------------------
        noches = (dto.fecha_checkout_esperado - dto.fecha_checkin_esperado).days
        total_estimado: Decimal = habitacion.tipo_habitacion.precio_por_noche * noches

        # ------------------------------------------------------------------
        # 5. Validar pago mínimo obligatorio (≥ 50%)
        # ------------------------------------------------------------------
        minimo_requerido = total_estimado * Decimal("0.50")
        if dto.monto_adelanto < minimo_requerido:
            raise ValueError(
                f"Se requiere un pago mínimo del 50% del total estimado "
                f"({minimo_requerido:.2f}) para confirmar la reserva. "
                f"Monto recibido: {dto.monto_adelanto:.2f}."
            )

        # ------------------------------------------------------------------
        # 6. Crear la reserva en estado CONFIRMADA
        # ------------------------------------------------------------------
        reserva = await self._reserva_repo.create(
            Reserva(
                habitacion_id=dto.habitacion_id,
                fecha_checkin_esperado=dto.fecha_checkin_esperado,
                fecha_checkout_esperado=dto.fecha_checkout_esperado,
                estado=EstadoReserva.CONFIRMADA,
            )
        )

        # ------------------------------------------------------------------
        # 7. Vincular huéspedes
        # ------------------------------------------------------------------
        await self._reserva_repo.agregar_huesped(
            reserva=reserva,
            huesped_id=dto.huesped_titular_id,
            es_titular=True,
        )
        for huesped_id in dto.huespedes_adicionales:
            await self._reserva_repo.agregar_huesped(
                reserva=reserva,
                huesped_id=huesped_id,
                es_titular=False,
            )

        # ------------------------------------------------------------------
        # 8. Registrar el adelanto
        # ------------------------------------------------------------------
        pago = await self._pago_repo.create(
            Pago(
                reserva_id=reserva.id,
                monto=dto.monto_adelanto,
                concepto=ConceptoPago.ADELANTO,
                metodo_pago=dto.metodo_pago,
                estado=EstadoPago.PAGADO,
            )
        )

        return ReservaConfirmadaDTO(
            reserva_id=reserva.id,
            estado=reserva.estado,
            total_estimado=total_estimado,
            pago_id=pago.id,
            mensaje="Reserva confirmada con pago de adelanto registrado.",
        )