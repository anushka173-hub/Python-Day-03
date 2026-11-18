from getpass import getpass

from sqlalchemy import select

from app.core.security import hash_password
from app.database.session import SessionLocal
from app.model.model import User
from app.repositories.user_repository import get_user_repository


def create_admin():
    db = SessionLocal()

    try:
        # Check whether an ADMIN account already exists.
        existing_admin = db.scalar(
            select(User).where(User.role == "ADMIN")
        )

        if existing_admin:
            print("An ADMIN account already exists.")
            return

        email = input("Enter ADMIN email: ").strip().lower()
        password = getpass("Enter ADMIN password: ")
        confirm_password = getpass("Confirm ADMIN password: ")

        if not email:
            print("Email cannot be empty.")
            return

        if len(password) < 8:
            print("Password must contain at least 8 characters.")
            return

        if password != confirm_password:
            print("Passwords do not match.")
            return

        hashed_password = hash_password(password)

        user_repository = get_user_repository()

        user_repository.create(
            db=db,
            email=email,
            hashed_password=hashed_password,
            role="ADMIN",
        )

        print("ADMIN account created successfully!")

    finally:
        db.close()


if __name__ == "__main__":
    create_admin()