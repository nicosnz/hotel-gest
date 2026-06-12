import uuid
from decimal import Decimal
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, model_validator

from models import MetodoPago
from repositories import HabitacionRepository, PagoRepository, ReservaRepository
from services.reservas.crearReserva import CrearReservaDTO, ReservaConfirmadaDTO, ReservaService
from db.postgres import get_db

router = APIRouter()



class CrearReservaRequest(BaseModel):
    habitacion_id: uuid.UUID
    fecha_checkin_esperado: date
    fecha_checkout_esperado: date
    huesped_titular_id: uuid.UUID
    huespedes_adicionales: list[uuid.UUID] = []
    monto_adelanto: Decimal
    metodo_pago: MetodoPago

    @model_validator(mode="after")
    def validar_fechas(self):
        if self.fecha_checkout_esperado <= self.fecha_checkin_esperado:
            raise ValueError(
                "La fecha de check-out debe ser posterior a la fecha de check-in."
            )
        return self


class ReservaConfirmadaResponse(BaseModel):
    reserva_id: uuid.UUID
    estado: str
    total_estimado: Decimal
    pago_id: uuid.UUID
    mensaje: str




async def get_reserva_service(
    session: AsyncSession = Depends(get_db),
) -> ReservaService:
    return ReservaService(
        reserva_repo=ReservaRepository(session),
        habitacion_repo=HabitacionRepository(session),
        pago_repo=PagoRepository(session),
    )




@router.post(
    "/",
    response_model=ReservaConfirmadaResponse,
    status_code=status.HTTP_201_CREATED,
)
async def crear_reserva(
    body: CrearReservaRequest,
    service: ReservaService = Depends(get_reserva_service),
) -> ReservaConfirmadaResponse:
    try:
        resultado: ReservaConfirmadaDTO = await service.crear_reserva(
            CrearReservaDTO(
                habitacion_id=body.habitacion_id,
                fecha_checkin_esperado=body.fecha_checkin_esperado,
                fecha_checkout_esperado=body.fecha_checkout_esperado,
                huesped_titular_id=body.huesped_titular_id,
                huespedes_adicionales=body.huespedes_adicionales,
                monto_adelanto=body.monto_adelanto,
                metodo_pago=body.metodo_pago,
            )
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )

    return ReservaConfirmadaResponse(
        reserva_id=resultado.reserva_id,
        estado=resultado.estado,
        total_estimado=resultado.total_estimado,
        pago_id=resultado.pago_id,
        mensaje=resultado.mensaje,
    )