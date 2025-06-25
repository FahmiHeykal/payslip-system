from fastapi import FastAPI
from app.api.v1 import admin, employee
from app.middlewares.logging_middleware import LoggingMiddleware

app = FastAPI(title="Payslip System")

app.add_middleware(LoggingMiddleware)

app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])
app.include_router(employee.router, prefix="/api/v1/employee", tags=["Employee"])
