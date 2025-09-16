from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from app.models.base import Base

class VisitorEvent(Base):
    __tablename__ = "visitor_events"

    id = Column(Integer, primary_key=True, index=True)
    visitor_id = Column(Integer, ForeignKey("visitors.id"), nullable=False)
    event_type = Column(String, nullable=False)  # e.g., "checkin", "checkout", "update"
    notes = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
