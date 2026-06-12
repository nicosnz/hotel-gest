import uuid
from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, field_validator
from sqlalchemy.ext.asyncio import AsyncSession

from repositories import ReservaRepository, ServicioRepository
from services.reservas.agregarConsumo import (
    ConsumoRegistradoDTO,
    ConsumoService,
    RegistrarConsumoDTO,
)
from db.postgres import get_db

router = APIRouter()


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class RegistrarConsumoRequest(BaseModel):
    reserva_id: uuid.UUID
    servicio_id: uuid.UUID
    cantidad: int

    @field_validator("cantidad")
    @classmethod
    def cantidad_positiva(cls, v: int) -> int:
        if v < 1:
            raise ValueError("La cantidad debe ser mayor a cero.")
        return v


class ConsumoRegistradoResponse(BaseModel):
    reserva_id: uuid.UUID
    servicio_id: uuid.UUID
    servicio_nombre: str
    cantidad: int
    precio_unitario: Decimal
    subtotal: Decimal
    fecha_consumo: datetime
    saldo_acumulado: Decimal
    mensaje: str


# ---------------------------------------------------------------------------
# Dependencia
# ---------------------------------------------------------------------------

async def get_consumo_service(
    session: AsyncSession = Depends(get_db),
) -> ConsumoService:
    return ConsumoService(
        reserva_repo=ReservaRepository(session),
        servicio_repo=ServicioRepository(session),
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post(
    "/",
    response_model=ConsumoRegistradoResponse,
    status_code=status.HTTP_201_CREATED,
)
async def registrar_consumo(
    body: RegistrarConsumoRequest,
    service: ConsumoService = Depends(get_consumo_service),
) -> ConsumoRegistradoResponse:
    try:
        resultado: ConsumoRegistradoDTO = await service.registrar_consumo(
            RegistrarConsumoDTO(
                reserva_id=body.reserva_id,
                servicio_id=body.servicio_id,
                cantidad=body.cantidad,
            )
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )

    return ConsumoRegistradoResponse(
        reserva_id=resultado.reserva_id,
        servicio_id=resultado.servicio_id,
        servicio_nombre=resultado.servicio_nombre,
        cantidad=resultado.cantidad,
        precio_unitario=resultado.precio_unitario,
        subtotal=resultado.subtotal,
        fecha_consumo=resultado.fecha_consumo,
        saldo_acumulado=resultado.saldo_acumulado,
        mensaje=resultado.mensaje,
    )