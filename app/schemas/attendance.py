from pydantic import BaseModel
from datetime import date

class AttendanceCreate(BaseModel):
    date: date

class AttendanceOut(BaseModel):
    id: int
    user_id: int
    date: date

    class Config:
        orm_mode = True
