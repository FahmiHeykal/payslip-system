from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime
from app.db.base import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String, nullable=False) 
    user_id = Column(Integer, nullable=True)
    ip_address = Column(String, nullable=True)
    request_id = Column(String, nullable=True)
    target_table = Column(String, nullable=False)
    target_id = Column(Integer, nullable=True)
    extra_data = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
