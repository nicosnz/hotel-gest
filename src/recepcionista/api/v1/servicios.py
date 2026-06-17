from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from repositories import ServicioRepository
from db.postgres import get_db

router = APIRouter()


class ServicioResponse(BaseModel):
    id: UUID
    nombre: str
    descripcion: str | None
    precio: Decimal
    activo: bool


async def get_servicio_repo(
    session: AsyncSession = Depends(get_db),
) -> ServicioRepository:
    return ServicioRepository(session)


@router.get(
    "/",
    response_model=list[ServicioResponse],
    status_code=status.HTTP_200_OK,
)
async def listar_servicios(
    repo: ServicioRepository = Depends(get_servicio_repo),
) -> list[ServicioResponse]:
    servicios = await repo.get_all()
    return [
        ServicioResponse(
            id=s.id,
            nombre=s.nombre,
            descripcion=s.descripcion,
            precio=s.precio,
            activo=s.activo,
        )
        for s in servicios
    ]
