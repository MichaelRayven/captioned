import uuid
from datetime import UTC, datetime, timedelta
from math import ceil
from typing import TYPE_CHECKING

from pydantic import HttpUrl

from app.core.config import settings

from .schemas import (
    AbortUploadRequest,
    CompleteUploadRequest,
    CompleteUploadResponse,
    InitiateUploadRequest,
    InitiateUploadResponse,
    PresignedPart,
)

if TYPE_CHECKING:
    from types_aiobotocore_s3 import S3Client


class FileUploadService:
    def __init__(self, client: S3Client) -> None:
        self.client = client

    def _generate_key(self, filename: str) -> str:
        return f'uploads/{uuid.uuid4()}/{filename}'

    def _get_parts_count(self, size: int) -> int:
        part_size = settings.s3.part_size_bytes
        parts_count = ceil(size / part_size)
        if parts_count > settings.s3.max_part_number:
            part_size = ceil(size / settings.s3.max_part_number)
            parts_count = settings.s3.max_part_number

        return parts_count

    async def initiate_multipart_upload(
        self, req: InitiateUploadRequest
    ) -> InitiateUploadResponse:
        key = self._generate_key(req.filename)
        upload = await self.client.create_multipart_upload(
            Bucket=settings.s3.bucket_name,
            Key=key,
            ContentType=req.content_type,
        )

        parts_count = self._get_parts_count(req.size)
        presigned_parts = []

        for part_number in range(1, parts_count + 1):
            url = await self.client.generate_presigned_url(
                ClientMethod='upload_part',
                Params={
                    'Bucket': settings.s3.bucket_name,
                    'Key': self._generate_key(req.filename),
                    'UploadId': upload['UploadId'],
                    'PartNumber': part_number,
                },
                ExpiresIn=settings.s3.presigned_url_expiry,
            )
            presigned_parts.append(
                PresignedPart(part_number=part_number, url=HttpUrl(url))
            )

        expires_at = datetime.now(UTC) + timedelta(
            seconds=settings.s3.presigned_url_expiry
        )
        return InitiateUploadResponse(
            upload_id=upload['UploadId'],
            key=key,
            parts=presigned_parts,
            expires_at=expires_at,
        )

    async def complete_multipart_upload(
        self, req: CompleteUploadRequest
    ) -> CompleteUploadResponse:
        response = await self.client.complete_multipart_upload(
            Bucket=settings.s3.bucket_name,
            Key=req.key,
            UploadId=req.upload_id,
            MultipartUpload={
                'Parts': [
                    {'ETag': part.etag, 'PartNumber': part.part_number}
                    for part in req.parts
                ]
            },
        )
        return CompleteUploadResponse(
            key=req.key, location=response['Location']
        )

    async def abort_multipart_upload(self, req: AbortUploadRequest) -> None:
        await self.client.abort_multipart_upload(
            Bucket=settings.s3.bucket_name,
            Key=req.key,
            UploadId=req.upload_id,
        )
