import os
import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.models import user, attendance, overtime, reimbursement, payroll

DB_NAME = f"test_{uuid.uuid4().hex}.db"
DB_URL = f"sqlite:///./{DB_NAME}"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    try:
        os.remove(DB_NAME)
    except PermissionError:
        pass

@pytest.fixture(scope="function")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture
def user_credentials():
    return {"username": f"user_{uuid.uuid4().hex[:6]}", "password": "pass123", "salary": 5000000}

@pytest.fixture
def admin_credentials():
    return {"username": f"admin_{uuid.uuid4().hex[:6]}", "password": "admin123", "salary": 8000000}

def get_token(client, credentials):
    client.post("/api/v1/employee/register", json=credentials)
    res = client.post("/api/v1/employee/login", data=credentials)
    return res.json()["access_token"]

def get_admin_token(client, credentials):
    register_data = credentials.copy()
    register_data.pop("is_admin", None)
    client.post("/api/v1/employee/register", json=register_data)

    res = client.post("/api/v1/employee/login", data=credentials)
    token = res.json()["access_token"]

    client.app.dependency_overrides = {}
    from app.db.session import get_db
    from app.models.user import User
    db = next(get_db())
    user = db.query(User).filter_by(username=register_data["username"]).first()
    user.is_admin = True
    db.commit()

    return token