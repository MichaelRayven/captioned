from typing import TYPE_CHECKING

from pydantic import BaseModel, Field, HttpUrl, model_validator

from app.core.config import settings

if TYPE_CHECKING:
    from datetime import datetime


class InitiateUploadRequest(BaseModel):
    filename: str
    content_type: str
    size: int = Field(gt=0, le=settings.s3.max_file_size_bytes)

    @model_validator(mode='after')
    def validate_upload(self) -> InitiateUploadRequest:
        if self.content_type not in settings.s3.allowed_content_types:
            raise ValueError(f'Unsupported content type: {self.content_type}')
        if self.size > settings.s3.max_file_size_bytes:
            raise ValueError('File exceeds maximum allowed size of 500 MB')

        return self


class CompleteUploadRequest(BaseModel):
    class UploadedPart(BaseModel):
        part_number: int = Field(ge=1, le=settings.s3.max_part_number)
        etag: str  # returned in the ETag header

    upload_id: str
    key: str
    parts: list[UploadedPart] = Field(min_length=1)


class AbortUploadRequest(BaseModel):
    upload_id: str
    key: str


class PresignedPart(BaseModel):
    part_number: int
    url: HttpUrl


class InitiateUploadResponse(BaseModel):
    upload_id: str
    key: str
    parts: list[PresignedPart]
    expires_at: datetime


class CompleteUploadResponse(BaseModel):
    key: str
    url: str
