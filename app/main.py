"""Application entry point.

Run from the employee_api folder:  uvicorn app.main:app --reload
Docs:                              http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI

from app.routers import employees
from app.routers import departments
from app.routers import leaves
from app.core.logging_config import setup_logging
import logging

setup_logging()

app = FastAPI()

app = FastAPI(
    title="Employee REST API",
    description="Assignment E - CRUD API for employees with filtering and validation.",
    version="1.0.0",
)

logger = logging.getLogger(__name__)
logger.info("Employee API application started")

app.include_router(employees.router)
app.include_router(departments.router)
app.include_router(leaves.router)
