from datetime import date
from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select

from models import Habitacion
from repositories import HabitacionRepository, ReservaRepository
from services.habitaciones.habitacionesDisponibles import DisponibilidadResultadoDTO, HabitacionService
from db.postgres import get_db

router = APIRouter()


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class HabitacionResponse(BaseModel):
    id: UUID
    numero: str
    piso: int
    tipo: str
    capacidad: int
    precio_por_noche: Decimal
    estado: str


class HabitacionDisponibleResponse(BaseModel):
    id: UUID
    numero: str
    piso: int
    tipo: str
    capacidad: int
    precio_por_noche: Decimal


class DisponibilidadResponse(BaseModel):
    fecha_checkin: date
    fecha_checkout: date
    noches: int
    habitaciones: list[HabitacionDisponibleResponse]
    mensaje: str


# ---------------------------------------------------------------------------
# Dependencia
# ---------------------------------------------------------------------------

async def get_habitacion_service(
    session: AsyncSession = Depends(get_db),
) -> HabitacionService:
    return HabitacionService(
        habitacion_repo=HabitacionRepository(session),
        reserva_repo=ReservaRepository(session),
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get(
    "/disponibilidad",
    response_model=DisponibilidadResponse,
    status_code=status.HTTP_200_OK,
)
async def consultar_disponibilidad(
    fecha_checkin: date = Query(..., description="Fecha de check-in (YYYY-MM-DD)"),
    fecha_checkout: date = Query(..., description="Fecha de check-out (YYYY-MM-DD)"),
    service: HabitacionService = Depends(get_habitacion_service),
) -> DisponibilidadResponse:
    try:
        resultado: DisponibilidadResultadoDTO = await service.consultar_disponibilidad(
            fecha_checkin=fecha_checkin,
            fecha_checkout=fecha_checkout,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )

    return DisponibilidadResponse(
        fecha_checkin=resultado.fecha_checkin,
        fecha_checkout=resultado.fecha_checkout,
        noches=resultado.noches,
        habitaciones=[
            HabitacionDisponibleResponse(
                id=h.id,
                numero=h.numero,
                piso=h.piso,
                tipo=h.tipo,
                capacidad=h.capacidad,
                precio_por_noche=h.precio_por_noche,
            )
            for h in resultado.habitaciones
        ],
        mensaje=resultado.mensaje,
    )


@router.get(
    "/",
    response_model=list[HabitacionResponse],
    status_code=status.HTTP_200_OK,
)
async def listar_habitaciones(
    session: AsyncSession = Depends(get_db),
) -> list[HabitacionResponse]:
    result = await session.execute(
        select(Habitacion).options(selectinload(Habitacion.tipo_habitacion))
    )
    habitaciones = result.scalars().all()
    return [
        HabitacionResponse(
            id=h.id,
            numero=h.numero,
            piso=h.piso,
            tipo=h.tipo_habitacion.nombre if h.tipo_habitacion else "—",
            capacidad=h.tipo_habitacion.capacidad if h.tipo_habitacion else 0,
            precio_por_noche=h.tipo_habitacion.precio_por_noche if h.tipo_habitacion else 0,
            estado=h.estado,
        )
        for h in habitaciones
    ]