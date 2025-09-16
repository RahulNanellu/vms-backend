from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.services.auth import hash_password  # add at top

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserOut)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    u = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),  # <-- hashed
        full_name=payload.full_name,
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    return u

@router.get("/", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()
