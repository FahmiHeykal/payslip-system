from sqlalchemy.orm import Session
from datetime import datetime
from app.models.overtime import Overtime
from fastapi import HTTPException

def has_existing_overtime(db: Session, user_id: int, date):
    return db.query(Overtime).filter(
        Overtime.user_id == user_id,
        Overtime.date == date
    ).first()

def create_overtime(db: Session, user_id: int, date, hours: float):
    if hours > 3:
        raise HTTPException(status_code=400, detail="Cannot submit more than 3 hours per day")

    if datetime.combine(date, datetime.min.time()) > datetime.now():
        raise HTTPException(status_code=400, detail="Cannot submit overtime in the future")

    if has_existing_overtime(db, user_id, date):
        raise HTTPException(status_code=400, detail="Overtime already submitted for this date")

    record = Overtime(user_id=user_id, date=date, hours=hours)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
