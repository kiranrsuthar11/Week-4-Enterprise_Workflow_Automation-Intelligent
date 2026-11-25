from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class RegisterIn(BaseModel):
    username: str = Field(min_length=3, max_length=80)
    password: str = Field(min_length=8, max_length=128)

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class DepartmentIn(BaseModel):
    name: str = Field(min_length=1, max_length=100)

class EmployeeIn(BaseModel):
    employee_code: str = Field(min_length=2, max_length=30)
    name: str = Field(min_length=1, max_length=120)
    email: str = Field(min_length=5, max_length=160)
    job_title: str = ""
    status: str = "Active"
    department_id: Optional[int] = None

class EmployeeOut(EmployeeIn):
    id: int
    model_config = ConfigDict(from_attributes=True)

class WorkflowIn(BaseModel):
    title: str = Field(min_length=1, max_length=180)
    description: str = Field(default="", max_length=2000)
    document_id: Optional[int] = None

class WorkflowDecision(BaseModel):
    decision: str = Field(min_length=1, max_length=10)
    note: str = Field(default="", max_length=1000)
