
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    HR = "HR"
    EMPLOYEE = "EMPLOYEE"


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    role: UserRole = UserRole.EMPLOYEE
    employee_id: Optional[int] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    user_id: int
    email: EmailStr
    role: UserRole
    employee_id: Optional[int] = None
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
