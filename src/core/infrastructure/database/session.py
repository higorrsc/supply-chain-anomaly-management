from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from src.core.infrastructure.config.settings import settings

connect_args: dict[str, bool] = (
    {"check_same_thread": False} if settings.test_in_memory else {}
)
poolclass = StaticPool if settings.test_in_memory else None

engine = create_async_engine(
    settings.database_url,
    echo=False,
    connect_args=connect_args,
    poolclass=poolclass,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db_session() -> AsyncGenerator[AsyncSession]:
    """Dependency to provide a database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
