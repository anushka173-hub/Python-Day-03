from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.model.model import User


class UserNotFoundError(Exception):
    def __init__(self, user_id: int):
        super().__init__(f"User with id {user_id} not found")
        self.user_id = user_id


class DuplicateUserEmailError(Exception):
    def __init__(self, email: str):
        super().__init__(
            f"A user with email '{email}' already exists"
        )
        self.email = email


class UserRepository:

    def get_by_email(self, db: Session, email: str) -> User | None:
        statement = select(User).where(
            func.lower(User.email) == email.strip().lower()
        )

        return db.scalar(statement)

    def get_by_id(self, db: Session, user_id: int) -> User:
        user = db.get(User, user_id)

        if user is None:
            raise UserNotFoundError(user_id)

        return user

    def create(
        self,
        db: Session,
        email: str,
        hashed_password: str,
        role: str,
        employee_id: int | None = None,
    ) -> User:

        email = email.strip().lower()

        existing_user = self.get_by_email(db, email)

        if existing_user is not None:
            raise DuplicateUserEmailError(email)

        user = User(
            email=email,
            hashed_password=hashed_password,
            role=role,
            employee_id=employee_id,
        )

        try:
            db.add(user)
            db.commit()
            db.refresh(user)

            return user

        except IntegrityError as exc:
            db.rollback()

            if self.get_by_email(db, email) is not None:
                raise DuplicateUserEmailError(email) from exc

            raise


_user_repository = UserRepository()


def get_user_repository() -> UserRepository:
    return _user_repository

