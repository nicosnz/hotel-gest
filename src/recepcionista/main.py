from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.v1 import reservas
from api.v1 import habitaciones
from api.v1 import checkIn
from api.v1 import consumo
from core import config
from redis.asyncio import Redis
import db.redis as cache


@asynccontextmanager
async def lifespan(app: FastAPI):
    cache.redis_client = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
    yield
    await cache.redis_client.close()

app = FastAPI(lifespan=lifespan)

app.include_router(reservas.router,prefix="/api/v1/reservas",tags=["reservas"])
app.include_router(habitaciones.router,prefix="/api/v1/habitaciones",tags=["habitaciones"])
app.include_router(checkIn.router,prefix="/api/v1/checkin",tags=["check in"])
app.include_router(consumo.router,prefix="/api/v1/consumos",tags=["consumos"])

@app.get("/api/v1/health")
async def health():
    return {"status": "ok"}

