from sqlalchemy.orm import Session
from datetime import date
from app.models.attendance import Attendance
from fastapi import HTTPException


def attendance_exists(db: Session, user_id: int, check_date: date) -> bool:
    return db.query(Attendance).filter(
        Attendance.user_id == user_id,
        Attendance.date == check_date
    ).first() is not None


def create_attendance(
    db: Session,
    user_id: int,
    attendance_date: date,
    created_by: int = None,
    ip_address: str = None,
    request_id: str = None,
):
    if attendance_date.weekday() >= 5:
        raise HTTPException(status_code=400, detail="Cannot submit attendance on weekends.")

    if attendance_exists(db, user_id, attendance_date):
        raise HTTPException(status_code=400, detail="Attendance already submitted for this day.")

    record = Attendance(
        user_id=user_id,
        date=attendance_date,
        created_by=created_by,
    )

    db.add(record)
    db.commit()
    db.refresh(record)
    return record
