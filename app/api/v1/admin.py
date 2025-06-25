from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.payroll import PayrollPeriodCreate, PayrollPeriodOut, PayrollSummaryOut
from app.services.auth_service import get_current_user, get_db
from app.crud.payroll import create_payroll_period, get_summary_for_period
from app.models.user import User

router = APIRouter()


@router.get("/test")
def test_admin():
    return {"message": "Admin route is working"}


@router.post("/payroll-period", response_model=PayrollPeriodOut)
def create_payroll(
    period: PayrollPeriodCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admin can create payroll periods")
    return create_payroll_period(db, period)


@router.get("/payroll-summary/{period_id}", response_model=PayrollSummaryOut)
def fetch_summary(
    period_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admin can view payroll summaries")
    return get_summary_for_period(db, payroll_period_id=period_id)
