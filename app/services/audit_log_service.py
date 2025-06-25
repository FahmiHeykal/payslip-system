from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog

def log_action(
    db: Session,
    action: str,
    user_id: int,
    ip_address: str,
    request_id: str,
    target_table: str,
    target_id: int = None,
    extra_data: dict = None
):
    log = AuditLog(
        action=action,
        user_id=user_id,
        ip_address=ip_address,
        request_id=request_id,
        target_table=target_table,
        target_id=target_id,
        extra_data=extra_data,
    )
    db.add(log)
    db.commit()
