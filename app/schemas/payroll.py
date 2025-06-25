from pydantic import BaseModel
from datetime import date
from typing import List

class PayrollPeriodCreate(BaseModel):
    start_date: date
    end_date: date

class PayrollPeriodOut(PayrollPeriodCreate):
    id: int
    is_processed: bool

    class Config:
        orm_mode = True

class PayrollSlipOut(BaseModel):
    id: int
    user_id: int
    payroll_period_id: int
    base_salary: float
    total_attendance_days: int
    attendance_deduction: float
    total_overtime_hours: float
    overtime_pay: float
    total_reimbursement: float
    take_home_pay: float

    class Config:
        orm_mode = True

class PayslipSummaryItem(BaseModel):
    user_id: int
    username: str
    take_home_pay: float

class PayrollSummaryOut(BaseModel):
    payroll_period_id: int
    total_paid: float
    details: List[PayslipSummaryItem]
