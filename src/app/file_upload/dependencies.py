from typing import Annotated

from fastapi import Depends

from app.file_upload.services import MultipartUploadService

MultipartUploadServiceDependency = Annotated[
    MultipartUploadService, Depends(MultipartUploadService)
]
