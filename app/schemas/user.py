from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    salary: float
    is_admin: Optional[bool] = False

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(UserBase):
    id: int
    is_admin: bool
    salary: float

    class Config:
        orm_mode = True
