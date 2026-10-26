
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.model.model import Employee, Leave
from app.leave_schemas import LeaveCreate


def create_leave(
    db: Session,
    employee_id: int,
    data: LeaveCreate,
) -> Leave:
    employee = db.get(Employee, employee_id)

    if employee is None:
        raise LookupError(f"Employee with id {employee_id} not found")

    leave = Leave(
        employee_id=employee_id,
        start_date=data.start_date,
        end_date=data.end_date,
        reason=data.reason.strip(),
    )

    db.add(leave)
    db.commit()
    db.refresh(leave)

    return leave


def get_employee_leaves(
    db: Session,
    employee_id: int,
) -> list[Leave]:
    employee = db.get(Employee, employee_id)

    if employee is None:
        raise LookupError(f"Employee with id {employee_id} not found")

    statement = (
        select(Leave)
        .where(Leave.employee_id == employee_id)
        .order_by(Leave.leave_id)
    )

    return list(db.scalars(statement).all())
