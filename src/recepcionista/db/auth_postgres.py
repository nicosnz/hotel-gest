from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from core import config

auth_engine = create_async_engine(config.AUTH_DB_URL, echo=False)
AuthAsyncSessionLocal = async_sessionmaker(auth_engine, expire_on_commit=False)


async def create_auth_tables():
    from models.usuario import Usuario
    async with auth_engine.begin() as conn:
        await conn.run_sync(
            Usuario.__table__.create,  # type: ignore[attr-defined]
            checkfirst=True,
        )


async def get_auth_db():
    async with AuthAsyncSessionLocal() as session:
        yield session
