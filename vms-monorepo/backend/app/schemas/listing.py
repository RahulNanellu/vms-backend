from pydantic import BaseModel
from typing import List
from app.schemas.visitor import VisitorOut

class PageMeta(BaseModel):
    page: int
    page_size: int
    total: int

class VisitorListResponse(BaseModel):
    items: List[VisitorOut]
    meta: PageMeta
