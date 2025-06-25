from sqlalchemy.orm import Session
from datetime import datetime
from app.models.reimbursement import Reimbursement

def create_reimbursement(db: Session, user_id: int, date, amount: float, description: str = None):
    if date > datetime.utcnow().date():
        raise ValueError("Cannot submit reimbursement for future dates")

    record = Reimbursement(
        user_id=user_id,
        date=date,
        amount=amount,
        description=description
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
