from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    salary = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    attendances = relationship(
        "Attendance",
        back_populates="user",
        foreign_keys="Attendance.user_id"
    )

    created_attendances = relationship(
        "Attendance",
        back_populates="creator",
        foreign_keys="Attendance.created_by"
    )