import uuid
from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from models import MetodoPago
from repositories import HabitacionRepository, PagoRepository, ReservaRepository
from services.reservas.checkout import CheckoutConfirmadoDTO, CheckoutDTO, CheckoutService
from db.postgres import get_db

router = APIRouter()


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class CheckoutRequest(BaseModel):
    reserva_id: uuid.UUID
    monto_pago: Decimal
    metodo_pago: MetodoPago


class CheckoutResponse(BaseModel):
    reserva_id: uuid.UUID
    habitacion_id: uuid.UUID
    costo_hospedaje: Decimal
    total_consumos: Decimal
    total_final: Decimal
    adelanto_pagado: Decimal
    saldo_pagado: Decimal
    fecha_checkout_real: datetime
    mensaje: str


# ---------------------------------------------------------------------------
# Dependencia
# ---------------------------------------------------------------------------

async def get_checkout_service(
    session: AsyncSession = Depends(get_db),
) -> CheckoutService:
    return CheckoutService(
        reserva_repo=ReservaRepository(session),
        habitacion_repo=HabitacionRepository(session),
        pago_repo=PagoRepository(session),
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post(
    "/",
    response_model=CheckoutResponse,
    status_code=status.HTTP_200_OK,
)
async def realizar_checkout(
    body: CheckoutRequest,
    service: CheckoutService = Depends(get_checkout_service),
) -> CheckoutResponse:
    try:
        resultado: CheckoutConfirmadoDTO = await service.realizar_checkout(
            CheckoutDTO(
                reserva_id=body.reserva_id,
                monto_pago=body.monto_pago,
                metodo_pago=body.metodo_pago,
            )
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )

    return CheckoutResponse(
        reserva_id=resultado.reserva_id,
        habitacion_id=resultado.habitacion_id,
        costo_hospedaje=resultado.costo_hospedaje,
        total_consumos=resultado.total_consumos,
        total_final=resultado.total_final,
        adelanto_pagado=resultado.adelanto_pagado,
        saldo_pagado=resultado.saldo_pagado,
        fecha_checkout_real=resultado.fecha_checkout_real,
        mensaje=resultado.mensaje,
    )