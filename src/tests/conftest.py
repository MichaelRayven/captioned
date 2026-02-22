from typing import TYPE_CHECKING

import pytest
from alembic.config import Config
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    AsyncTransaction,
)

from alembic import command
from app.config import settings
from app.db.base import engine
from app.deps import get_async_session
from app.main import app

# Test database connection settings
# change host, user, password, etc...
settings.postgres.database = 'test_db'

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator, Generator


# Required per https://anyio.readthedocs.io/en/stable/testing.html#using-async-fixtures-with-higher-scopes
@pytest.fixture(scope='session')
def anyio_backend() -> str:
    return 'asyncio'


@pytest.fixture(scope='session', autouse=True)
def run_migrations() -> Generator[None]:
    """
    Run Alembic migrations once before any tests start.
    """
    alembic_cfg = Config('alembic.ini')

    command.upgrade(alembic_cfg, 'head')

    yield

    command.downgrade(alembic_cfg, 'base')


@pytest.fixture(scope='session')
async def connection(anyio_backend: str) -> AsyncGenerator[AsyncConnection]:  # noqa: ARG001
    async with engine.connect() as connection:
        yield connection


@pytest.fixture
async def transaction(
    connection: AsyncConnection,
) -> AsyncGenerator[AsyncTransaction]:
    async with connection.begin() as transaction:
        yield transaction


@pytest.fixture
async def session(
    connection: AsyncConnection, transaction: AsyncTransaction
) -> AsyncGenerator[AsyncSession]:
    async_session = AsyncSession(
        bind=connection,
        join_transaction_mode='create_savepoint',
    )

    yield async_session

    await transaction.rollback()


# All changes that occur in a test function are rolled back
# after function exits, even if session.commit() is called
# in FastAPI's application endpoints
@pytest.fixture
async def client(
    connection: AsyncConnection, transaction: AsyncTransaction
) -> AsyncGenerator[AsyncClient]:
    """Get HTTPX client for API testing."""

    async def override_get_async_session() -> AsyncGenerator[AsyncSession]:
        async_session = AsyncSession(
            bind=connection,
            join_transaction_mode='create_savepoint',
        )
        async with async_session:
            yield async_session

    app.dependency_overrides[get_async_session] = override_get_async_session

    yield AsyncClient(transport=ASGITransport(app=app), base_url='http://test')
    del app.dependency_overrides[get_async_session]

    await transaction.rollback()
