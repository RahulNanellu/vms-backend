from datetime import datetime, timedelta, timezone
from typing import Optional
from passlib.context import CryptContext
from jose import jwt, JWTError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
JWT_SECRET = "***REMOVED***"   # TODO: put in .env later
JWT_ALG = "HS256"
JWT_EXPIRE_MIN = 60 * 24

def hash_password(raw: str) -> str: return pwd_context.hash(raw)
def verify_password(raw: str, hashed: str) -> bool: return pwd_context.verify(raw, hashed)

def create_access_token(sub: str, expires_minutes: int = JWT_EXPIRE_MIN) -> str:
    now = datetime.now(timezone.utc); exp = now + timedelta(minutes=expires_minutes)
    payload = {"sub": sub, "iat": int(now.timestamp()), "exp": int(exp.timestamp())}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)

def decode_token(token: str) -> Optional[dict]:
    try: return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
    except JWTError: return None
