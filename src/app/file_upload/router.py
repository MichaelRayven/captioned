from typing import TYPE_CHECKING

from fastapi import APIRouter

from .schemas import (
    AbortUploadRequest,
    CompleteUploadRequest,
    CompleteUploadResponse,
    InitiateUploadRequest,
    InitiateUploadResponse,
)

if TYPE_CHECKING:
    from .dependencies import MultipartUploadServiceDependency

router = APIRouter(prefix='/files', tags=['files'])


@router.post('/upload/initiate', response_model=InitiateUploadResponse)
async def initiate_multipart_upload(
    body: InitiateUploadRequest,
    service: MultipartUploadServiceDependency,
) -> InitiateUploadResponse:
    """Start a multipart upload. Returns presigned PUT URLs for every part."""
    return await service.initiate_multipart_upload(body)


@router.post('/upload/complete', response_model=CompleteUploadResponse)
async def complete_multipart_upload(
    body: CompleteUploadRequest,
    service: MultipartUploadServiceDependency,
) -> CompleteUploadResponse:
    """Assemble all uploaded parts into the final S3 object."""
    return await service.complete_multipart_upload(body)


@router.delete('/upload/abort', status_code=204)
async def abort_multipart_upload(
    body: AbortUploadRequest,
    service: MultipartUploadServiceDependency,
) -> None:
    """Cancel an in-progress multipart upload."""
    await service.abort_multipart_upload(body)
