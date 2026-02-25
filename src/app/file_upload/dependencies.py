from typing import Annotated

from fastapi import Depends

from app.file_upload.services import FileUploadService

FileUploadServiceDependency = Annotated[
    FileUploadService, Depends(FileUploadService)
]
