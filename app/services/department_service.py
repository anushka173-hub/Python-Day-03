
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories import department_repository


def create_department(db: Session, name: str, description: str | None):
    name = name.strip()

    if not name:
        raise ValueError("Department name cannot be empty.")

    existing = department_repository.get_by_name(db, name)

    if existing:
        raise ValueError("A department with this name already exists.")

    try:
        department = department_repository.create(
            db,
            name,
            description,
        )
        db.commit()
        db.refresh(department)
        return department

    except IntegrityError as exc:
        db.rollback()
        raise ValueError(
            "Department name already exists or violates a database constraint."
        ) from exc

    except Exception:
        db.rollback()
        raise


def list_departments(db: Session):
    return department_repository.get_all(db)
