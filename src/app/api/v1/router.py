from fastapi.routing import APIRouter

from app.file_upload.router import router as file_upload_router

router = APIRouter(prefix='/api/v1')
router.include_router(file_upload_router)
