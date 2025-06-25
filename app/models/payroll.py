from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime, JSON, Date, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class PayrollPeriod(Base):
    __tablename__ = "payroll_periods"

    id = Column(Integer, primary_key=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_processed = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PayrollSlip(Base):
    __tablename__ = "payroll_slips"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    payroll_period_id = Column(Integer, ForeignKey("payroll_periods.id"))

    base_salary = Column(Float)
    total_attendance_days = Column(Integer)
    attendance_deduction = Column(Float)

    total_overtime_hours = Column(Float)
    overtime_pay = Column(Float)

    total_reimbursement = Column(Float)
    take_home_pay = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User")
    payroll_period = relationship("PayrollPeriod")
