from fastapi import APIRouter
from .weather import api_router as weather_api_router

router = APIRouter(prefix="/api/v1")

router.include_router(weather_api_router.router)

@router.get("/")
def api_root():
    return {"msg": "API v1 route reached"}
