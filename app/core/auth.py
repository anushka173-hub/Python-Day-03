import os

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.model.model import User
from app.repositories.user_repository import get_user_repository


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:

    secret_key = os.getenv("SECRET_KEY")
    algorithm = os.getenv("ALGORITHM", "HS256")

    if not secret_key:
        raise RuntimeError("SECRET_KEY is missing from .env")

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=[algorithm],
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        user_id = int(user_id)

    except (InvalidTokenError, ValueError, TypeError):
        raise credentials_exception

    user_repository = get_user_repository()

    try:
        user = user_repository.get_by_id(db, user_id)
    except Exception:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is inactive",
        )

    return user


def require_roles(*allowed_roles: str):

    def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:

        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )

        return current_user

    return role_checker