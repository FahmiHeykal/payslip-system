from sqlalchemy import Column, Integer, ForeignKey, Date, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Overtime(Base):
    __tablename__ = "overtimes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    hours = Column(Float, nullable=False)  # maksimal 3 jam

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", backref="overtimes")
