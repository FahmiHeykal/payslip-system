from app.db.session import SessionLocal
from app.crud.user import create_user
from app.schemas.user import UserCreate
from app.models.user import User
from faker import Faker

def seed_users():
    db = SessionLocal()
    fake = Faker()

    try:
        print("Seeding started...")

        if not db.query(User).filter_by(username="admin").first():
            admin = UserCreate(
                username="admin",
                password="admin123",
                salary=10000000,
                is_admin=True
            )
            create_user(db, admin)
            print("Admin user created.")
        else:
            print("Admin user already exists.")

        for i in range(10): 
            username = f"user{i}"
            if not db.query(User).filter_by(username=username).first():
                user = UserCreate(
                    username=username,
                    password="password123",
                    salary=fake.random_int(min=5000000, max=15000000),
                    is_admin=False
                )
                create_user(db, user)

        print("Regular users created.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_users()
