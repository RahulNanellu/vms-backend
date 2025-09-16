from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...db import get_db, Base, engine
from ...models import models as m

router = APIRouter(prefix="/admin", tags=["admin"])
Base.metadata.create_all(bind=engine)

@router.post("/society/create")
def create_society(name: str, db: Session = Depends(get_db)):
    s = m.Society(name=name)
    db.add(s); db.commit(); db.refresh(s)
    return {"id": s.id, "name": s.name, "is_active": s.is_active}

@router.post("/society/{society_id}/toggle")
def toggle_society(society_id: int, enable: bool, db: Session = Depends(get_db)):
    s = db.get(m.Society, society_id)
    if not s: return {"error":"not found"}
    s.is_active = enable
    db.commit()
    return {"id": s.id, "is_active": s.is_active}
