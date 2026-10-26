"""HTTP layer: routes, query parameters and status codes."""

from typing import Optional
import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi import status as http_status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repository import (
    DuplicateEmailError,
    EmployeeNotFoundError,
    EmployeeRepository,
    InvalidDepartmentError,
    get_repository,
)
from app.schemas import EmployeeCreate, EmployeeResponse, EmployeeStatus

router = APIRouter(prefix="/employees", tags=["employees"])
logger = logging.getLogger(__name__)


def _not_found(exc: Exception) -> HTTPException:
    return HTTPException(
        status_code=http_status.HTTP_404_NOT_FOUND,
        detail=str(exc),
    )


def _duplicate(exc: Exception) -> HTTPException:
    return HTTPException(
        status_code=http_status.HTTP_409_CONFLICT,
        detail=str(exc),
    )



@router.get("", response_model=list[EmployeeResponse])
def list_employees(
    department_id: Optional[int] = Query(
        None, description="Filter by department"
    ),
    status: Optional[EmployeeStatus] = Query(
        None, description="ACTIVE or INACTIVE"
    ),
    min_salary: Optional[float] = Query(
        None, ge=0, description="Minimum salary"
    ),
    page: int = Query(
        1, ge=1, description="Page number"
    ),
    limit: int = Query(
        50, ge=1, le=100, description="Records per page (maximum 100)"
    ),
    db: Session = Depends(get_db),
    repo: EmployeeRepository = Depends(get_repository),
):

    logger.info("Listing employees")

    return repo.list(
        db,
        department_id=department_id,
        status=status,
        min_salary=min_salary,
        page=page,
        limit=limit,
    )


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    repo: EmployeeRepository = Depends(get_repository),
):
    try:
        return repo.get(db, employee_id)
    except EmployeeNotFoundError as exc:
        raise _not_found(exc) from exc



@router.post(
    "",
    response_model=EmployeeResponse,
    status_code=http_status.HTTP_201_CREATED,
)
def create_employee(
    payload: EmployeeCreate,
    db: Session = Depends(get_db),
    repo: EmployeeRepository = Depends(get_repository),
):
    try:
        employee = repo.create(db, payload)

        logger.info("Employee created successfully")
        return employee

    except DuplicateEmailError as exc:
        logger.warning("Employee creation failed: duplicate email")
        raise _duplicate(exc) from exc

    except InvalidDepartmentError as exc:
        logger.warning("Employee creation failed: invalid department")
        raise _not_found(exc) from exc

    except IntegrityError as exc:
        logger.warning("Employee creation failed: database constraint")
        raise HTTPException(
            status_code=http_status.HTTP_409_CONFLICT,
            detail="Employee data conflicts with a database constraint.",
        ) from exc




@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    payload: EmployeeCreate,
    db: Session = Depends(get_db),
    repo: EmployeeRepository = Depends(get_repository),
):
    try:
        employee = repo.update(db, employee_id, payload)

        logger.info(
            "Employee updated successfully | employee_id=%s",
            employee_id,
        )
        return employee

    except EmployeeNotFoundError as exc:
        logger.warning(
            "Employee update failed: employee not found | employee_id=%s",
            employee_id,
        )
        raise _not_found(exc) from exc

    except DuplicateEmailError as exc:
        logger.warning(
            "Employee update failed: duplicate email | employee_id=%s",
            employee_id,
        )
        raise _duplicate(exc) from exc

    except InvalidDepartmentError as exc:
        logger.warning(
            "Employee update failed: invalid department | employee_id=%s",
            employee_id,
        )
        raise _not_found(exc) from exc

    except IntegrityError as exc:
        logger.warning(
            "Employee update failed: database constraint | employee_id=%s",
            employee_id,
        )
        raise HTTPException(
            status_code=http_status.HTTP_409_CONFLICT,
            detail="Employee data conflicts with a database constraint.",
        ) from exc



@router.delete(
    "/{employee_id}",
    status_code=http_status.HTTP_204_NO_CONTENT,
)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    repo: EmployeeRepository = Depends(get_repository),
):
    try:
        repo.delete(db, employee_id)
        logger.info(
            "Employee deleted successfully | employee_id=%s",
            employee_id,
        )
    except EmployeeNotFoundError as exc:
        logger.warning(
            "Employee deletion failed: employee not found | employee_id=%s",
            employee_id,
        )
        raise _not_found(exc) from exc