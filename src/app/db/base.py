from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.config import settings


class Base(AsyncAttrs, DeclarativeBase):
    pass


engine = create_async_engine(
    url=str(settings.postgres.url),
    echo=settings.postgres.echo,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=settings.postgres.pool_size,
    max_overflow=settings.postgres.pool_max_overflow,
)

# Session factory
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
