import os
from datetime import datetime, timedelta, timezone
from app.config import settings
import jwt
from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.repositories import user_repository
from app.repositories.user_repository import (
    UserRepository,
    get_user_repository,
)


class InvalidCredentialsError(Exception):
    pass


class InactiveUserError(Exception):
    pass


class AuthService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def authenticate_user(
        self,
        db: Session,
        email: str,
        password: str,
    ):
        user = self.user_repository.get_by_email(db, email)

        # Do not reveal whether the email or password was incorrect.
        if user is None or not verify_password(
            password,
            user.hashed_password,
        ):
            raise InvalidCredentialsError("Invalid email or password")

        if not user.is_active:
            raise InactiveUserError("This account is inactive")

        return user

    def create_access_token(self, user_id: int) -> str:
        secret_key = settings.SECRET_KEY

        if not secret_key:
            raise RuntimeError("SECRET_KEY is missing from .env")

        algorithm = os.getenv("ALGORITHM", "HS256")
        expiry_minutes = int(
            os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
        )

        expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=expiry_minutes
        )

        payload = {
            "sub": str(user_id),
            "exp": expires_at,
        }

        return jwt.encode(
            payload,
            secret_key,
            algorithm=algorithm,
        )


_auth_service = AuthService(get_user_repository())


def get_auth_service() -> AuthService:
    return _auth_service

def get_all_Users(db, skip=0, limit=10):

    return user_repository.get_all_employees(
        db,
        skip=skip,
        limit=limit
    )