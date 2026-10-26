"""Pydantic models: request/response shapes and validation rules."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, Field, field_validator
from sqlalchemy.orm import DeclarativeBase



class Base(DeclarativeBase):
    pass



class EmployeeStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class EmployeeBase(BaseModel):
    name: str = Field(..., description="Employee name (must not be empty)")
    email: EmailStr
    salary: float = Field(..., ge=0, description="Salary (must not be negative)")
    department_id: int = Field(..., description="Department ID (must be an integer)")
    status: EmployeeStatus = EmployeeStatus.ACTIVE

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Name must not be empty")
        return v


class EmployeeCreate(EmployeeBase):
    """Request body for POST and PUT."""


class EmployeeResponse(EmployeeBase):
    """Response model: adds server-generated fields."""

    employee_id: int
    created_at: datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict

class EmployeeCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    department_id: int
    salary: float = Field(gt=0)        # Day 5: "invalid salary" test

class EmployeeOut(EmployeeCreate):
    employee_id: int
    status: str
    model_config = ConfigDict(from_attributes=True)

    