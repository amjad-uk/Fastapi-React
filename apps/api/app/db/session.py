from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from ..core.config import settings
ASYNC_URL = settings.DATABASE_URL.replace("postgresql+psycopg://", "postgresql+asyncpg://")
engine = create_async_engine(ASYNC_URL, future=True, pool_pre_ping=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
async def get_session() -> AsyncSession:
    async with SessionLocal() as session: yield session
