from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from pydantic import BaseModel

from db.auth_postgres import get_auth_db
from models.usuario import Usuario
from auth.jwt import verify_password, create_access_token

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    nombre: str
    apellido: str
    username: str


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(
    body: LoginRequest,
    session: AsyncSession = Depends(get_auth_db),
) -> TokenResponse:
    result = await session.execute(select(Usuario).where(Usuario.username == body.username))
    user = result.scalars().first()

    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
        )

    if not user.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo",
        )

    token = create_access_token(user.username, user.nombre, user.apellido)
    return TokenResponse(
        access_token=token,
        nombre=user.nombre,
        apellido=user.apellido,
        username=user.username,
    )
