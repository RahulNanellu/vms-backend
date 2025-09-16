from fastapi import APIRouter
router = APIRouter()

@router.get("/ping")
def ping_admin():
    return {"admin": "ok"}
