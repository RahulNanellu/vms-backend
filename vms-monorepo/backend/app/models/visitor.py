from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from app.models.base import Base

class Visitor(Base):
    __tablename__ = "visitors"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=True, index=True)
    phone = Column(String(50), nullable=True)
    company = Column(String(255), nullable=True)
    host_name = Column(String(255), nullable=True)
    visit_reason = Column(String(500), nullable=True)

    checked_in_at = Column(DateTime, server_default=func.now(), nullable=False)
    checked_out_at = Column(DateTime, nullable=True)
    is_checked_out = Column(Boolean, default=False, nullable=False)

    # NEW: who created this visitor
    created_by_user_id = Column(Integer, nullable=True, index=True)
