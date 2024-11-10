from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")

@router.get("/")
def api_root():
    return {"msg": "API v1 route reached"}
