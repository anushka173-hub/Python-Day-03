
from sqlalchemy.orm import Session

from app.leave_schemas import LeaveCreate
from app.repositories import leave_repository


def create_leave(
    db: Session,
    employee_id: int,
    data: LeaveCreate,
):
    return leave_repository.create_leave(db, employee_id, data)


def get_employee_leaves(db: Session, employee_id: int):
    return leave_repository.get_employee_leaves(db, employee_id)
