from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from fastapi import FastAPI

from app.db.base import close_db, init_db

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:  # noqa: ARG001
    await init_db()
    yield
    await close_db()


app = FastAPI(lifespan=lifespan)


@app.get('/healthcheck')
async def healthcheck() -> None:
    return
