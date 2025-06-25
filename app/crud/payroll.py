from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException
from datetime import timedelta

from app.models.user import User
from app.models.attendance import Attendance
from app.models.overtime import Overtime
from app.models.reimbursement import Reimbursement
from app.models.payroll import PayrollPeriod, PayrollSlip
from app.schemas.payroll import PayrollPeriodCreate


def create_payroll_period(db: Session, data: PayrollPeriodCreate):
    period = PayrollPeriod(
        start_date=data.start_date,
        end_date=data.end_date
    )
    db.add(period)
    db.commit()
    db.refresh(period)
    return period

def run_payroll_for_period(db: Session, period_id: int):
    period = db.query(PayrollPeriod).filter(PayrollPeriod.id == period_id).first()
    if not period:
        raise HTTPException(status_code=404, detail="Payroll period not found")
    if period.is_processed:
        raise HTTPException(status_code=400, detail="Payroll has already been processed")

    start_date = period.start_date
    end_date = period.end_date

    working_days = [start_date + timedelta(days=i) 
                    for i in range((end_date - start_date).days + 1) 
                    if (start_date + timedelta(days=i)).weekday() < 5]

    users = db.query(User).filter(User.is_admin == False).all()

    for user in users:
        salary_per_day = user.salary / len(working_days)

        attendances = db.query(Attendance).filter(
            and_(
                Attendance.user_id == user.id,
                Attendance.date.between(start_date, end_date)
            )
        ).all()

        overtime = db.query(Overtime).filter(
            and_(
                Overtime.user_id == user.id,
                Overtime.date.between(start_date, end_date)
            )
        ).all()

        reimbursements = db.query(Reimbursement).filter(
            and_(
                Reimbursement.user_id == user.id,
                Reimbursement.date.between(start_date, end_date)
            )
        ).all()

        present_days = len(attendances)
        total_overtime = sum([o.hours for o in overtime])
        total_reimbursement = sum([r.amount for r in reimbursements])

        attendance_deduction = (len(working_days) - present_days) * salary_per_day
        overtime_pay = total_overtime * salary_per_day * 2
        take_home_pay = user.salary - attendance_deduction + overtime_pay + total_reimbursement

        slip = PayrollSlip(
            user_id=user.id,
            payroll_period_id=period.id,
            base_salary=user.salary,
            total_attendance_days=present_days,
            attendance_deduction=attendance_deduction,
            total_overtime_hours=total_overtime,
            overtime_pay=overtime_pay,
            total_reimbursement=total_reimbursement,
            take_home_pay=take_home_pay
        )
        db.add(slip)

    period.is_processed = True
    db.commit()
    return {"status": "Payroll processed"}

def get_user_payslips(db: Session, user_id: int):
    return db.query(PayrollSlip).filter(PayrollSlip.user_id == user_id).all()

def get_summary_for_period(db: Session, payroll_period_id: int):
    slips = db.query(
        PayrollSlip.user_id,
        User.username,
        PayrollSlip.take_home_pay
    ).join(User).filter(PayrollSlip.payroll_period_id == payroll_period_id).all()

    total = sum([s.take_home_pay for s in slips])

    return {
        "payroll_period_id": payroll_period_id,
        "total_paid": total,
        "details": [
            {
                "user_id": s.user_id,
                "username": s.username,
                "take_home_pay": s.take_home_pay
            }
            for s in slips
        ]
    }