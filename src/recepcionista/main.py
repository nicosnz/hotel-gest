from fastapi import FastAPI
from contextlib import asynccontextmanager

from core import config
from redis.asyncio import Redis
import db.redis as cache


@asynccontextmanager
async def lifespan(app: FastAPI):
    cache.redis_client = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
    yield
    await cache.redis_client.close()

app = FastAPI(lifespan=lifespan)


@app.get("/api/v1/health")
async def health():
    return {"status": "ok"}

