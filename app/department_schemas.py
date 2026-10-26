from pydantic import BaseModel, ConfigDict, Field


class DepartmentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=255)


class DepartmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    department_id: int
    name: str
    description: str | None
