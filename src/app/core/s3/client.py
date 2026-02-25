from typing import TYPE_CHECKING

from aioboto3 import Session

from app.core.config import settings

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from types_aiobotocore_s3 import S3Client

session = Session()


async def get_client() -> AsyncGenerator[S3Client]:
    async with session.client(
        's3',
        endpoint_url=str(settings.s3.endpoint_url),
        aws_access_key_id=settings.s3.access_key_id,
        aws_secret_access_key=settings.s3.secret_key.get_secret_value(),
        region_name='ignore',
    ) as client:
        # Ensure bucket exists
        try:
            await client.head_bucket(Bucket=settings.s3.bucket_name)
        except client.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchBucket':
                await client.create_bucket(Bucket=settings.s3.bucket_name)
            else:
                raise

        yield client
