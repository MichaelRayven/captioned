from typing import TYPE_CHECKING

from app.db.base import async_session_factory

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from sqlalchemy.ext.asyncio import AsyncSession


async def get_async_session() -> AsyncGenerator[AsyncSession]:
    async with async_session_factory.begin() as session:
        yield session
