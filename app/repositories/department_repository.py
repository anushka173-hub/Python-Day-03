
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.model.model import Department


def get_by_name(db: Session, name: str):
    statement = select(Department).where(
        Department.name == name
    )
    return db.scalar(statement)


def get_all(db: Session):
    statement = select(Department).order_by(
        Department.department_id
    )
    return list(db.scalars(statement).all())


def create(db: Session, name: str, description: str | None):
    department = Department(
        name=name,
        description=description,
    )
    db.add(department)
    db.flush()
    return department
