import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from repositories import HuespedRepository
from services.huespedes.huespedes import CrearHuespedDTO, HuespedDTO, HuespedService
from db.postgres import get_db

router = APIRouter()


class CrearHuespedRequest(BaseModel):
    nombre: str
    apellido: str
    documento_identidad: str
    correo: Optional[str] = None
    telefono: Optional[str] = None


class HuespedResponse(BaseModel):
    id: uuid.UUID
    nombre: str
    apellido: str
    documento_identidad: str
    correo: Optional[str]
    telefono: Optional[str]


async def get_huesped_service(
    session: AsyncSession = Depends(get_db),
) -> HuespedService:
    return HuespedService(huesped_repo=HuespedRepository(session))


@router.post(
    "/",
    response_model=HuespedResponse,
    status_code=status.HTTP_201_CREATED,
)
async def crear_huesped(
    body: CrearHuespedRequest,
    service: HuespedService = Depends(get_huesped_service),
) -> HuespedResponse:
    try:
        resultado: HuespedDTO = await service.crear_huesped(
            CrearHuespedDTO(
                nombre=body.nombre,
                apellido=body.apellido,
                documento_identidad=body.documento_identidad,
                correo=body.correo,
                telefono=body.telefono,
            )
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    return HuespedResponse(**resultado.__dict__)


@router.get(
    "/",
    response_model=list[HuespedResponse],
    status_code=status.HTTP_200_OK,
)
async def listar_huespedes(
    service: HuespedService = Depends(get_huesped_service),
) -> list[HuespedResponse]:
    huespedes = await service.listar_huespedes()
    return [HuespedResponse(**h.__dict__) for h in huespedes]
