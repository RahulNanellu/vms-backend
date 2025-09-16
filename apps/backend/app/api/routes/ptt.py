from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from ...db import get_db, Base, engine
from ...models import models as m
from ...schemas.schemas import PTTIn, PTTOut
from ...services.queue import enqueue_ptt
from ...services.s3 import get_s3, ensure_bucket
import os, uuid, shutil

router = APIRouter(prefix="/ptt", tags=["ptt"])
Base.metadata.create_all(bind=engine)

@router.post("/message", response_model=PTTOut)
async def upload_ptt_message(
    group: str = Form(...),
    sender: str = Form(...),
    duration_sec: int = Form(...),
    priority: str = Form("NORMAL"),
    media: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # LoRa policy: enforce 20s cap (IP can be longer; client should choose path)
    if duration_sec > 20 and priority == "LOW":
        raise HTTPException(status_code=400, detail="LoRa clips must be ≤ 20s")

    ensure_bucket()
    s3 = get_s3()
    key = f"ptt/{uuid.uuid4()}_{media.filename}"
    local_dir = "/app/data/uploads"
    os.makedirs(local_dir, exist_ok=True)
    local_path = os.path.join(local_dir, key.replace("/", "_"))
    with open(local_path, "wb") as f:
        shutil.copyfileobj(media.file, f)

    with open(local_path, "rb") as f:
        s3.upload_fileobj(f, os.environ.get("S3_BUCKET", "vms-media"), key)

    rec = m.PTTMessage(group=group, sender=sender, media_url=key, duration_sec=duration_sec, priority=m.Priority(priority))
    db.add(rec); db.commit(); db.refresh(rec)

    # Queue background fan‑out / store‑and‑forward
    enqueue_ptt(rec.priority.value, "apps.worker.jobs:fanout_ptt", args=(rec.id,))

    return rec
