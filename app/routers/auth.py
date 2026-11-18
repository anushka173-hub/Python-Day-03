from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth_schemas import Token, UserResponse
from app.core.auth import get_current_user
from app.database.session import get_db
from app.model.model import User
from app.services.auth_service import (
    AuthService,
    InvalidCredentialsError,
    InactiveUserError,
    get_auth_service,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        user = auth_service.authenticate_user(
            db,
            form_data.username,
            form_data.password,
        )

        access_token = auth_service.create_access_token(user.user_id)

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except InactiveUserError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account is inactive",
        )


@router.get("/me", response_model=UserResponse)
def get_my_account(
    current_user: User = Depends(get_current_user),
):
    return current_user