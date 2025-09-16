from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.services.auth import verify_password, hash_password, create_access_token, decode_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.post("/signup", response_model=UserOut)
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    u = User(email=payload.email, hashed_password=hash_password(payload.password), full_name=payload.full_name)
    db.add(u); db.commit(); db.refresh(u)
    return u

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    u = db.query(User).filter(User.email == form.username).first()
    if not u or not verify_password(form.password, u.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"access_token": create_access_token(sub=str(u.id)), "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    data = decode_token(token)
    if not data or "sub" not in data: raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.get(User, int(data["sub"]))
    if not user or not user.is_active: raise HTTPException(status_code=401, detail="Inactive user")
    return user

@router.get("/me", response_model=UserOut)
def me(current: User = Depends(get_current_user)): return current
