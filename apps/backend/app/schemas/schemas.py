from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

class VisitorCreate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None

class VisitorOut(BaseModel):
    id: int
    name: Optional[str]
    phone: Optional[str]
    photo_url: Optional[str]
    created_at: datetime
    class Config:
        from_attributes = True

class VisitLogCreate(BaseModel):
    unit_id: int
    visitor_id: int
    gps_lat: Optional[float] = None
    gps_lon: Optional[float] = None
    photo_url: Optional[str] = None
    approved: bool = False
    gate_guard: Optional[str] = None

class VisitLogOut(BaseModel):
    id: int
    unit_id: int
    visitor_id: int
    approved: bool
    gps_lat: Optional[float]
    gps_lon: Optional[float]
    photo_url: Optional[str]
    created_at: datetime
    class Config:
        from_attributes = True

class PTTIn(BaseModel):
    group: str
    sender: str
    duration_sec: int = Field(ge=1, le=120)
    priority: Literal["HIGH","NORMAL","LOW"] = "NORMAL"

class PTTOut(BaseModel):
    id: int
    group: str
    sender: str
    media_url: str
    duration_sec: int
    priority: str
    created_at: datetime
    class Config:
        from_attributes = True
