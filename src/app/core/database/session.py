from typing import TYPE_CHECKING

from .base import session_factory

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from sqlalchemy.ext.asyncio import AsyncSession


async def get_async_session() -> AsyncGenerator[AsyncSession]:
    async with session_factory() as session:
        yield session
