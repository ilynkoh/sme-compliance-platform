from fastapi import APIRouter
from app.config import settings

router = APIRouter()

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }

@router.get("/config")
async def get_config():
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.FASTAPI_ENV,
        "debug": settings.DEBUG
    }