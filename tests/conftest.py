from collections.abc import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.infrastructure.config.settings import settings

settings.test_in_memory = True

# fmt: off
from src.core.infrastructure.database import AsyncSessionLocal, Base, engine  # noqa: E402, I001
# fmt: on


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_database() -> AsyncGenerator[None]:
    """Fixture that provides database setup"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession]:
    """
    Fixture that provides an AsyncSession connected
    to an in-memory SQLite database.
    """
    async with AsyncSessionLocal() as session:
        yield session
