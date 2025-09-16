from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from ...db import get_db, Base, engine
from ...models import models as m
from ...schemas.schemas import VisitorCreate, VisitorOut, VisitLogCreate, VisitLogOut
from ...services.s3 import get_s3, ensure_bucket
import os, uuid, shutil

router = APIRouter(prefix="/visitors", tags=["visitors"])

Base.metadata.create_all(bind=engine)

@router.post("/", response_model=VisitorOut)
def create_visitor(payload: VisitorCreate, db: Session = Depends(get_db)):
    v = m.Visitor(name=payload.name, phone=payload.phone)
    db.add(v); db.commit(); db.refresh(v)
    return v

@router.post("/photo", response_model=VisitorOut)
async def create_visitor_with_photo(
    name: str | None = Form(None),
    phone: str | None = Form(None),
    photo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    ensure_bucket()
    s3 = get_s3()
    key = f"photos/{uuid.uuid4()}_{photo.filename}"
    # Also store locally for dev
    local_dir = "/app/data/uploads"
    os.makedirs(local_dir, exist_ok=True)
    local_path = os.path.join(local_dir, key.replace("/", "_"))
    with open(local_path, "wb") as f:
        shutil.copyfileobj(photo.file, f)

    # Upload to S3/MinIO
    with open(local_path, "rb") as f:
        s3.upload_fileobj(f, os.environ.get("S3_BUCKET", "vms-media"), key)

    v = m.Visitor(name=name, phone=phone, photo_url=key)
    db.add(v); db.commit(); db.refresh(v)
    return v

@router.post("/log", response_model=VisitLogOut)
def log_visit(payload: VisitLogCreate, db: Session = Depends(get_db)):
    log = m.VisitLog(**payload.model_dump())
    db.add(log); db.commit(); db.refresh(log)
    return log
