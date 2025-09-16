from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db import Base
import enum

class Society(Base):
    __tablename__ = "societies"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Unit(Base):
    __tablename__ = "units"
    id = Column(Integer, primary_key=True)
    society_id = Column(Integer, ForeignKey("societies.id"))
    number = Column(String, nullable=False)
    resident_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    society = relationship("Society")

class Visitor(Base):
    __tablename__ = "visitors"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    phone = Column(String, nullable=True, index=True)
    photo_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class VisitLog(Base):
    __tablename__ = "visit_logs"
    id = Column(Integer, primary_key=True)
    unit_id = Column(Integer, ForeignKey("units.id"))
    visitor_id = Column(Integer, ForeignKey("visitors.id"))
    approved = Column(Boolean, default=False)
    gate_guard = Column(String, nullable=True)
    gps_lat = Column(Float, nullable=True)
    gps_lon = Column(Float, nullable=True)
    photo_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Priority(str, enum.Enum):
    HIGH = "HIGH"
    NORMAL = "NORMAL"
    LOW = "LOW"

class PTTMessage(Base):
    __tablename__ = "ptt_messages"
    id = Column(Integer, primary_key=True)
    group = Column(String, nullable=False, index=True)
    sender = Column(String, nullable=False)
    # path to audio clip (wav/ogg/mp3 < 20s for LoRa, no hard cap for IP)
    media_url = Column(String, nullable=False)
    duration_sec = Column(Integer, nullable=False)
    priority = Column(Enum(Priority), default=Priority.NORMAL)
    created_at = Column(DateTime, default=datetime.utcnow)
