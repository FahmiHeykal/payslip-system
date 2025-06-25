from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.models import user, attendance, overtime, reimbursement, payroll
