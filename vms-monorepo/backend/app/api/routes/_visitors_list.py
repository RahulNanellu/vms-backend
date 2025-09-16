from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from datetime import datetime
from app.db import SessionLocal
from app.models.visitor import Visitor
from app.schemas.visitor import VisitorOut
from app.schemas.listing import VisitorListResponse, PageMeta

router = APIRouter()

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/", response_model=VisitorListResponse)
def list_visitors(
    db: Session = Depends(get_db),
    active_only: bool = False,
    q: str | None = Query(None, description="Search first/last/email/company/host"),
    host_name: str | None = None,
    company: str | None = None,
    start: datetime | None = Query(None, description="ISO datetime, checked_in_at >= start"),
    end: datetime | None = Query(None, description="ISO datetime, checked_in_at <= end"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
):
    stmt = select(Visitor)
    where = []
    if active_only:
        where.append(Visitor.is_checked_out == False)  # noqa: E712
    if host_name:
        where.append(Visitor.host_name.ilike(f"%{host_name}%"))
    if company:
        where.append(Visitor.company.ilike(f"%{company}%"))
    if q:
        like = f"%{q}%"
        where.append(
            (Visitor.first_name.ilike(like)) |
            (Visitor.last_name.ilike(like))  |
            (Visitor.email.ilike(like))      |
            (Visitor.company.ilike(like))    |
            (Visitor.host_name.ilike(like))
        )
    if start:
        where.append(Visitor.checked_in_at >= start)
    if end:
        where.append(Visitor.checked_in_at <= end)
    for cond in where:
        stmt = stmt.where(cond)

    stmt = stmt.order_by(Visitor.checked_in_at.desc())
    total = db.execute(select(func.count()).select_from(stmt.subquery())).scalar_one()
    offset = (page - 1) * page_size
    items = list(db.execute(stmt.offset(offset).limit(page_size)).scalars())
    return VisitorListResponse(items=items, meta=PageMeta(page=page, page_size=page_size, total=total))
