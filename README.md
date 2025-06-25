# Payslip System - FastAPI + PostgreSQL

This is a scalable web-based payroll system designed to handle employee attendance, overtime, reimbursements, and payslip generation automatically and efficiently. Built with FastAPI and PostgreSQL, it includes full audit logging, request tracking, and automated testing.

In this employee :
- Works a regular 8-hour schedule (9AM - 5PM), Monday to Friday.
- Has their salary prorated based on attendance days within a payroll period.
- Can request overtime (up to 3 hours/day) which is paid at 2x the prorated hourly rate.
- Can submit reimbursements with amount and description.
- Receives a breakdown of all components in their payslip.

The admin :
- Defines payroll periods by specifying start and end dates.
- Runs payroll once per period.
- Can view a summary of total take-home pay for all employees.

## Features

### Employee Features
- Register and login with JWT authentication.
- Submit attendance (only on weekdays, once per day).
- Submit overtime (after work hours, max 3 hours/day, any day).
- Submit reimbursements (with amount and description).
- Generate and view a detailed payslip.

### Admin Features
- Add payroll period (start_date and end_date).
- Run payroll for a specific period (once only).
- View payroll summary across all employees.

## API Endpoints

### Authentication
- `POST /api/v1/employee/register`
- `POST /api/v1/employee/login`

### Attendance
- `POST /api/v1/employee/attendance`

### Overtime
- `POST /api/v1/employee/overtime`

### Reimbursement
- `POST /api/v1/employee/reimbursement`

### Payslip
- `GET /api/v1/employee/payslips`

### Admin Payroll
- `POST /api/v1/admin/payroll-period`
- `POST /api/v1/employee/payroll-run/{payroll_period_id}`
- `GET /api/v1/admin/payroll-summary/{payroll_period_id}`

## Role Access

|               Endpoint                      | Role     | Access       |
|---------------------------------------------|----------|--------------|
| Register & Login                            | Employee | Allowed      |
| Submit Attendance, Overtime, Reimbursement  | Employee | Allowed      |
| View Payslip                                | Employee | Allowed      |
| Create Payroll Period                       | Admin    | Allowed      |
| Run Payroll                                 | Admin    | Allowed      |
| View Payroll Summary                        | Admin    | Allowed      |

## Database Seeding

The `seed.py` script creates:
- 100 fake employees with usernames `user1` to `user100`
- 1 admin with username `admin` and password `adminpass`

To seed the database :

```bash
python seed.py
```

## Technology Stack

- Python 3.11

- FastAPI

- PostgreSQL

- SQLAlchemy

- Pydantic

- Pytest

## Automated Testing
This project includes unit and integration tests using pytest.

### Run all tests :

```bash 
pytest -v
```

##Test folder structure :

tests/
├── test_attendance.py
├── test_auth.py
├── test_overtime.py
├── test_payroll.py
├── test_payslip.py
├── test_reimbursement.py
├── test_summary.py
└── conftest.py

All features are covered and verified through automated tests.

## Advanced Features

- created_at and updated_at timestamps on all records

- created_by and updated_by fields for traceability

- Request IP address is logged for every user action

- Audit log table to record all critical changes

- Middleware to inject unique request_id into logs

## Run Locally
### Clone the repository :
```bash
git clone https://github.com/your-username/payslip-system.git
cd payslip-system
```

### Create a virtual environment :
```bash
python -m venv venv
source venv/bin/activate  
On Windows: venv\Scripts\activate
```

### Install dependencies :
```bash 
pip install -r requirements.txt`
```

### Run database migration :
```bash
alembic upgrade head`
```

###Start the application :
```bash
uvicorn app.main:app --reload`
```

### Seed fake data :
```bash
python seed.py
```

### Access API documentation :
```bash
- Swagger : ``http://localhost:8000/docs``
- ReDoc : ``http://localhost:8000/redoc``
```
