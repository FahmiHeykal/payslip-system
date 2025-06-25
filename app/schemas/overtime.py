from pydantic import BaseModel, Field
from datetime import date

class OvertimeCreate(BaseModel):
    date: date
    hours: float = Field(..., gt=0, le=3, description="Overtime hours (max 3 hours)")

class OvertimeOut(OvertimeCreate):
    id: int
    user_id: int

    class Config:
        orm_mode = True
