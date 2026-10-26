
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.leave_schemas import LeaveCreate, LeaveRead
from app.services import leave_service

router = APIRouter(
    prefix="/employees/{employee_id}/leave",
    tags=["Leaves"],
)


@router.post("", response_model=LeaveRead, status_code=201)
def create_leave(
    employee_id: int,
    payload: LeaveCreate,
    db: Session = Depends(get_db),
):
    try:
        return leave_service.create_leave(db, employee_id, payload)
    except LookupError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@router.get("", response_model=list[LeaveRead])
def get_employee_leaves(
    employee_id: int,
    db: Session = Depends(get_db),
):
    try:
        return leave_service.get_employee_leaves(db, employee_id)
    except LookupError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc
