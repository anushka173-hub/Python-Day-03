
from sqlalchemy import (
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    func,
)
from sqlalchemy.orm import relationship

from app.database.session import Base


class Department(Base):
    __tablename__ = "departments"

    department_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255), nullable=True)

    employees = relationship("Employee", back_populates="department")


class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    salary = Column(Numeric(12, 2), nullable=False)
    status = Column(String(20), nullable=False, default="ACTIVE")
    department_id = Column(
        Integer,
        ForeignKey("departments.department_id"),
        nullable=False,
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    department = relationship("Department", back_populates="employees")
    leaves = relationship(
        "Leave",
        back_populates="employee",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Leave(Base):
    __tablename__ = "leaves"

    leave_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(
        Integer,
        ForeignKey("employees.employee_id", ondelete="CASCADE"),
        nullable=False,
    )
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    reason = Column(String(255), nullable=False)
    status = Column(String(20), nullable=False, default="PENDING")
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    employee = relationship("Employee", back_populates="leaves")
