
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field, model_validator


class LeaveCreate(BaseModel):
    start_date: date
    end_date: date
    reason: str = Field(min_length=1, max_length=255)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_date < self.start_date:
            raise ValueError("End date must be on or after start date.")
        return self


class LeaveRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    leave_id: int
    employee_id: int
    start_date: date
    end_date: date
    reason: str
    status: str
    created_at: datetime
