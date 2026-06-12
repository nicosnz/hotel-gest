import uuid
from decimal import Decimal
from datetime import date,datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, model_validator

from models import MetodoPago,EstadoReserva
from repositories import HabitacionRepository, PagoRepository, ReservaRepository,ServicioRepository
from services.reservas.crearReserva import CrearReservaDTO, ReservaConfirmadaDTO, ReservaService
from services.reservas.obtenerReservas import ReservaQueryService, ReservaResumenDTO
from services.reservas.obtenerConsumoPorReserva import (
    ConsultaConsumoService,
    ConsumosReservaDTO,
)

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
class HuespedResumenResponse(BaseModel):
    id: uuid.UUID
    nombre: str
    apellido: str
    documento_identidad: str
    es_titular: bool


class ConsumoResumenResponse(BaseModel):
    servicio_nombre: str
    cantidad: int
    precio_unitario: Decimal
    subtotal: Decimal
    fecha_consumo: datetime


class ReservaResumenResponse(BaseModel):
    id: uuid.UUID
    habitacion_numero: str
    estado: EstadoReserva
    fecha_checkin_esperado: date
    fecha_checkout_esperado: date
    fecha_checkin_real: datetime | None
    fecha_checkout_real: datetime | None
    observaciones: str | None
    huespedes: list[HuespedResumenResponse]
    consumos: list[ConsumoResumenResponse]
 




def _reserva_to_response(r: ReservaResumenDTO) -> ReservaResumenResponse:
    return ReservaResumenResponse(
        id=r.id,
        habitacion_numero=r.habitacion_numero,
        estado=r.estado,
        fecha_checkin_esperado=r.fecha_checkin_esperado,
        fecha_checkout_esperado=r.fecha_checkout_esperado,
        fecha_checkin_real=r.fecha_checkin_real,
        fecha_checkout_real=r.fecha_checkout_real,
        observaciones=r.observaciones,
        huespedes=[
            HuespedResumenResponse(
                id=h.id,
                nombre=h.nombre,
                apellido=h.apellido,
                documento_identidad=h.documento_identidad,
                es_titular=h.es_titular,
            )
            for h in r.huespedes
        ],
        consumos=[
            ConsumoResumenResponse(
                servicio_nombre=c.servicio_nombre,
                cantidad=c.cantidad,
                precio_unitario=c.precio_unitario,
                subtotal=c.subtotal,
                fecha_consumo=c.fecha_consumo,
            )
            for c in r.consumos
        ],
    )


async def get_reserva_service(
    session: AsyncSession = Depends(get_db),
) -> ReservaService:
    return ReservaService(
        reserva_repo=ReservaRepository(session),
        habitacion_repo=HabitacionRepository(session),
        pago_repo=PagoRepository(session),
    )
async def get_reserva_query_service(
    session: AsyncSession = Depends(get_db),
) -> ReservaQueryService:
    return ReservaQueryService(
        reserva_repo=ReservaRepository(session),
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

class ConsumoDetalleResponse(BaseModel):
    servicio_id: uuid.UUID
    servicio_nombre: str
    cantidad: int
    precio_unitario: Decimal
    subtotal: Decimal
    fecha_consumo: datetime
 
 
class ConsumosReservaResponse(BaseModel):
    reserva_id: uuid.UUID
    estado_reserva: EstadoReserva
    consumos: list[ConsumoDetalleResponse]
    total_acumulado: Decimal
    mensaje: str
 
 
# ---------------------------------------------------------------------------
# Dependencia
# ---------------------------------------------------------------------------
 
async def get_consulta_consumo_service(
    session: AsyncSession = Depends(get_db),
) -> ConsultaConsumoService:
    return ConsultaConsumoService(
        reserva_repo=ReservaRepository(session),
        servicio_repo=ServicioRepository(session),
    )
 
 
# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
 
@router.get(
    "/{reserva_id}/consumos",
    response_model=ConsumosReservaResponse,
    status_code=status.HTTP_200_OK,
)
async def consultar_consumos(
    reserva_id: uuid.UUID,
    service: ConsultaConsumoService = Depends(get_consulta_consumo_service),
) -> ConsumosReservaResponse:
    try:
        resultado: ConsumosReservaDTO = await service.consultar_consumos(reserva_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
 
    return ConsumosReservaResponse(
        reserva_id=resultado.reserva_id,
        estado_reserva=resultado.estado_reserva,
        consumos=[
            ConsumoDetalleResponse(
                servicio_id=c.servicio_id,
                servicio_nombre=c.servicio_nombre,
                cantidad=c.cantidad,
                precio_unitario=c.precio_unitario,
                subtotal=c.subtotal,
                fecha_consumo=c.fecha_consumo,
            )
            for c in resultado.consumos
        ],
        total_acumulado=resultado.total_acumulado,
        mensaje=resultado.mensaje,
    )
 
@router.get(
    "/",
    response_model=list[ReservaResumenResponse],
    status_code=status.HTTP_200_OK,
)
async def listar_reservas(
    service: ReservaQueryService = Depends(get_reserva_query_service),
) -> list[ReservaResumenResponse]:
    resultados: list[ReservaResumenDTO] = await service.listar_reservas()
    return [_reserva_to_response(r) for r in resultados]
 
 
@router.get(
    "/{reserva_id}",
    response_model=ReservaResumenResponse,
    status_code=status.HTTP_200_OK,
)
async def obtener_reserva(
    reserva_id: uuid.UUID,
    service: ReservaQueryService = Depends(get_reserva_query_service),
) -> ReservaResumenResponse:
    try:
        resultado: ReservaResumenDTO = await service.obtener_reserva(reserva_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
 
    return _reserva_to_response(resultado)
 
