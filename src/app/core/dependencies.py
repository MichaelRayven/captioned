from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from types_aiobotocore_s3 import S3Client

from app.core.database import get_async_session
from app.core.s3.client import get_client

AsyncSessionDependency = Annotated[AsyncSession, Depends(get_async_session)]
AsyncS3ClientDependency = Annotated[S3Client, Depends(get_client)]
