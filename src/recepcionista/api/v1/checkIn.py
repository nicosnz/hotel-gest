import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from models.reserva import EstadoReserva
from repositories.reserva import ReservaRepository
from services.reservas.checkIn import CheckinConfirmadoDTO, CheckinDTO, CheckinService
from db.postgres import get_db

router = APIRouter()


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class CheckinRequest(BaseModel):
    reserva_id: uuid.UUID
    huesped_id: uuid.UUID


class CheckinResponse(BaseModel):
    reserva_id: uuid.UUID
    huesped_id: uuid.UUID
    fecha_checkin_real: datetime
    estado: EstadoReserva
    mensaje: str


# ---------------------------------------------------------------------------
# Dependencia
# ---------------------------------------------------------------------------

async def get_checkin_service(
    session: AsyncSession = Depends(get_db),
) -> CheckinService:
    return CheckinService(
        reserva_repo=ReservaRepository(session),
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post(
    "/",
    response_model=CheckinResponse,
    status_code=status.HTTP_200_OK,
)
async def registrar_checkin(
    body: CheckinRequest,
    service: CheckinService = Depends(get_checkin_service),
) -> CheckinResponse:
    try:
        resultado: CheckinConfirmadoDTO = await service.registrar_checkin(
            CheckinDTO(
                reserva_id=body.reserva_id,
                huesped_id=body.huesped_id,
            )
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )

    return CheckinResponse(
        reserva_id=resultado.reserva_id,
        huesped_id=resultado.huesped_id,
        fecha_checkin_real=resultado.fecha_checkin_real,
        estado=resultado.estado,
        mensaje=resultado.mensaje,
    )