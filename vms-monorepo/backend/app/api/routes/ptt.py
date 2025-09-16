from fastapi import APIRouter
router = APIRouter()

@router.get("/ping")
def ping_ptt():
    return {"ptt": "ok"}
