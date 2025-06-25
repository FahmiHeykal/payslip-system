from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.user import UserOut, UserCreate
from app.schemas.attendance import AttendanceCreate, AttendanceOut
from app.schemas.overtime import OvertimeCreate, OvertimeOut
from app.schemas.reimbursement import ReimbursementCreate, ReimbursementOut
from app.schemas.payroll import PayrollSlipOut
from app.crud import (
    user as user_crud,
    attendance as attendance_crud,
    overtime as overtime_crud,
    reimbursement as reimbursement_crud,
    payroll as payroll_crud,
)
from app.services.auth_service import create_access_token, get_db, get_current_user
from app.services.audit_log_service import log_action
from app.models.user import User

router = APIRouter()

@router.get("/test")
def test_employee():
    return {"message": "Employee route is working"}

@router.post("/register", response_model=UserOut)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    return user_crud.create_user(db, user)

@router.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = user_crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/attendance", response_model=AttendanceOut)
def submit_attendance(
    attendance: AttendanceCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = attendance_crud.create_attendance(db, user_id=current_user.id, attendance_date=attendance.date)

    log_action(
        db=db,
        action="CREATE_ATTENDANCE",
        user_id=current_user.id,
        ip_address=request.state.ip,
        request_id=request.state.request_id,
        target_table="attendances",
        target_id=record.id,
        extra_data={"date": str(attendance.date)},
    )

    return record

@router.post("/overtime", response_model=OvertimeOut)
def submit_overtime(
    overtime: OvertimeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return overtime_crud.create_overtime(db, user_id=current_user.id, date=overtime.date, hours=overtime.hours)

@router.post("/reimbursement", response_model=ReimbursementOut)
def submit_reimbursement(
    reimbursement: ReimbursementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return reimbursement_crud.create_reimbursement(
        db,
        user_id=current_user.id,
        date=reimbursement.date,
        amount=reimbursement.amount,
        description=reimbursement.description,
    )

@router.post("/payroll-run/{period_id}")
def run_payroll(
    period_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admin can run payroll")
    return payroll_crud.run_payroll_for_period(db, period_id=period_id)

@router.get("/payslips", response_model=List[PayrollSlipOut])
def get_user_payslips_list(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return payroll_crud.get_user_payslips(db, user_id=current_user.id)
