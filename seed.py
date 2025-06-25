import random
from faker import Faker
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from datetime import datetime

fake = Faker()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def seed_users(db: Session):
    if db.query(User).first():
        print("Database already seeded.")
        return

    for _ in range(100):
        username = fake.user_name()
        password = hash_password("password123")
        salary = random.randint(3_000_000, 10_000_000)
        user = User(
            username=username,
            password_hash=password,
            salary=salary,
            is_admin=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(user)

    admin = User(
        username="admin",
        password_hash=hash_password("admin123"),
        salary=0,
        is_admin=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(admin)

    db.commit()
    print("Seeding complete: 100 users + 1 admin.")

if __name__ == "__main__":
    db = SessionLocal()
    seed_users(db)
    db.close()
