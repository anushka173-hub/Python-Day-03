from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.model.model import Department, Employee
from app.schemas import EmployeeCreate, EmployeeStatus


class EmployeeNotFoundError(Exception):
    def __init__(self, employee_id: int):
        super().__init__(f"Employee with id {employee_id} not found")
        self.employee_id = employee_id


class DuplicateEmailError(Exception):
    def __init__(self, email: str):
        super().__init__(
            f"An employee with email '{email}' already exists"
        )
        self.email = email


class InvalidDepartmentError(Exception):
    def __init__(self, department_id: int):
        super().__init__(
            f"Department with id {department_id} not found"
        )
        self.department_id = department_id



class EmployeeRepository:

    def list(
        self,
        db: Session,
        department_id: int | None = None,
        status: EmployeeStatus | None = None,
        min_salary: float | None = None,
        page: int = 1,
        limit: int = 50,
    ) -> list[Employee]:
        statement = select(Employee)

        if department_id is not None:
            statement = statement.where(
                Employee.department_id == department_id
            )

        if status is not None:
            statement = statement.where(Employee.status == status)

        if min_salary is not None:
            statement = statement.where(Employee.salary >= min_salary)

        offset = (page - 1) * limit

        statement = (
            statement
            .order_by(Employee.employee_id)
            .offset(offset)
            .limit(limit)
        )

        return list(db.scalars(statement).all())

    def get(self, db: Session, employee_id: int) -> Employee:
        employee = db.get(Employee, employee_id)

        if employee is None:
            raise EmployeeNotFoundError(employee_id)

        return employee

    def _email_taken(
        self,
        db: Session,
        email: str,
        exclude_id: int | None = None,
    ) -> bool:
        statement = select(Employee.employee_id).where(
            func.lower(Employee.email) == email.strip().lower()
        )

        if exclude_id is not None:
            statement = statement.where(
                Employee.employee_id != exclude_id
            )

        return db.scalar(statement) is not None

    def create(self, db: Session, data: EmployeeCreate) -> Employee:
        email = data.email.strip()

        if self._email_taken(db, email):
            raise DuplicateEmailError(email)

        department = db.get(Department, data.department_id)

        if department is None:
            raise InvalidDepartmentError(data.department_id)

        employee = Employee(
            **{
                **data.model_dump(),
                "email": email,
            }
        )

        try:
            db.add(employee)
            db.commit()
            db.refresh(employee)
            return employee

        except IntegrityError as exc:
            db.rollback()

            if self._email_taken(db, email):
                raise DuplicateEmailError(email) from exc

            raise

    def update(
        self,
        db: Session,
        employee_id: int,
        data: EmployeeCreate,
    ) -> Employee:
        employee = self.get(db, employee_id)
        email = data.email.strip()

        if self._email_taken(db, email, exclude_id=employee_id):
            raise DuplicateEmailError(email)

        department = db.get(Department, data.department_id)

        if department is None:
            raise InvalidDepartmentError(data.department_id)

        for field, value in data.model_dump().items():
            setattr(employee, field, value)

        employee.email = email

        try:
            db.commit()
            db.refresh(employee)
            return employee

        except IntegrityError:
            db.rollback()
            raise

    def delete(self, db: Session, employee_id: int) -> None:
        employee = self.get(db, employee_id)

        try:
            db.delete(employee)
            db.commit()
        except Exception:
            db.rollback()
            raise


_repository = EmployeeRepository()


def get_repository() -> EmployeeRepository:
    return _repository
