
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.department_schemas import DepartmentCreate, DepartmentRead
from app.services.department_service import (
    create_department,
    list_departments,
)

router = APIRouter(prefix="/departments", tags=["Departments"])


@router.post(
    "",
    response_model=DepartmentRead,
    status_code=status.HTTP_201_CREATED,
)
def create_department_endpoint(
    data: DepartmentCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_department(
            db,
            data.name,
            data.description,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.get("", response_model=list[DepartmentRead])
def get_departments_endpoint(
    db: Session = Depends(get_db),
):
    return list_departments(db)
