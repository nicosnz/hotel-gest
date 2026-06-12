from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from api.v1 import reservas, habitaciones, huespedes, servicios, checkIn, consumo, checkout
from api.v1 import auth as auth_router
from auth.dependencies import get_current_user
from core import config
from redis.asyncio import Redis
import db.redis as cache
from db.auth_postgres import create_auth_tables, AuthAsyncSessionLocal
from models.usuario import Usuario
from auth.jwt import hash_password
from sqlmodel import select


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Redis
    cache.redis_client = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)

    # Auth DB: crear tabla y usuario inicial si no existe
    await create_auth_tables()
    async with AuthAsyncSessionLocal() as session:
        result = await session.execute(select(Usuario).limit(1))
        if not result.scalars().first():
            user = Usuario(
                username=config.AUTH_INITIAL_USERNAME,
                password_hash=hash_password(config.AUTH_INITIAL_PASSWORD),
                nombre="Recepcionista",
                apellido="Principal",
            )
            session.add(user)
            await session.commit()

    yield

    await cache.redis_client.close()


app = FastAPI(lifespan=lifespan)

protected = [Depends(get_current_user)]

app.include_router(auth_router.router,    prefix="/api/v1/auth",        tags=["auth"])
app.include_router(reservas.router,       prefix="/api/v1/reservas",     tags=["reservas"],     dependencies=protected)
app.include_router(habitaciones.router,   prefix="/api/v1/habitaciones", tags=["habitaciones"], dependencies=protected)
app.include_router(huespedes.router,      prefix="/api/v1/huespedes",    tags=["huespedes"],    dependencies=protected)
app.include_router(servicios.router,      prefix="/api/v1/servicios",    tags=["servicios"],    dependencies=protected)
app.include_router(checkIn.router,        prefix="/api/v1/checkin",      tags=["check-in"],     dependencies=protected)
app.include_router(consumo.router,        prefix="/api/v1/consumos",     tags=["consumos"],     dependencies=protected)
app.include_router(checkout.router,       prefix="/api/v1/checkout",     tags=["check-out"],    dependencies=protected)


@app.get("/api/v1/health")
async def health():
    return {"status": "ok"}
