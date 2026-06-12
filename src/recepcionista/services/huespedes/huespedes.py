from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Optional

from models import Huesped
from repositories import HuespedRepository


@dataclass
class CrearHuespedDTO:
    nombre: str
    apellido: str
    documento_identidad: str
    correo: Optional[str] = None
    telefono: Optional[str] = None


@dataclass
class HuespedDTO:
    id: uuid.UUID
    nombre: str
    apellido: str
    documento_identidad: str
    correo: Optional[str]
    telefono: Optional[str]


class HuespedService:
    def __init__(self, huesped_repo: HuespedRepository) -> None:
        self._repo = huesped_repo

    async def crear_huesped(self, dto: CrearHuespedDTO) -> HuespedDTO:
        existente = await self._repo.get_by_documento(dto.documento_identidad)
        if existente:
            raise ValueError(
                f"Ya existe un huésped con el documento '{dto.documento_identidad}'."
            )
        huesped = await self._repo.create(
            Huesped(
                nombre=dto.nombre,
                apellido=dto.apellido,
                documento_identidad=dto.documento_identidad,
                correo=dto.correo,
                telefono=dto.telefono,
            )
        )
        return self._to_dto(huesped)

    async def listar_huespedes(self) -> list[HuespedDTO]:
        huespedes = await self._repo.get_all()
        return [self._to_dto(h) for h in huespedes]

    def _to_dto(self, h: Huesped) -> HuespedDTO:
        return HuespedDTO(
            id=h.id,
            nombre=h.nombre,
            apellido=h.apellido,
            documento_identidad=h.documento_identidad,
            correo=h.correo,
            telefono=h.telefono,
        )
