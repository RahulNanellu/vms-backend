from datetime import datetime
from pydantic import BaseModel, Field, EmailStr

class VisitorBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str  = Field(min_length=1, max_length=100)
    email: EmailStr | None = None
    phone: str | None = None
    company: str | None = None
    host_name: str | None = None
    visit_reason: str | None = None

class VisitorCreate(VisitorBase):
    pass

class VisitorUpdate(BaseModel):
    # all optional for PATCH
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str  | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None
    phone: str | None = None
    company: str | None = None
    host_name: str | None = None
    visit_reason: str | None = None

class VisitorOut(VisitorBase):
    id: int
    checked_in_at: datetime
    checked_out_at: datetime | None = None
    is_checked_out: bool

    class Config:
        from_attributes = True
