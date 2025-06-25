from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class ReimbursementCreate(BaseModel):
    date: date
    amount: float = Field(..., gt=0)
    description: Optional[str] = None

class ReimbursementOut(ReimbursementCreate):
    id: int
    user_id: int

    class Config:
        orm_mode = True
