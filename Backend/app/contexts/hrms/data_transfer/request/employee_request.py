from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal
from datetime import date

EmploymentType = Literal["permanent", "contract"]
SalaryType = Literal["monthly", "daily", "hourly"]

class ContractSchema(BaseModel):
    start_date: date
    end_date: date
    salary_type: SalaryType
    rate: float = Field(..., gt=0)
    leave_policy_id: Optional[str] = None
    pay_on_holiday: bool = True
    pay_on_weekend: bool = False

class EmployeeCreateSchema(BaseModel):
    employee_code: str = Field(..., min_length=2, max_length=30)
    full_name: str = Field(..., min_length=2, max_length=120)
    department: Optional[str] = None
    position: Optional[str] = None

    employment_type: EmploymentType = "contract"
    contract: Optional[ContractSchema] = None

    # optional links / metadata
    manager_user_id: Optional[str] = None
    schedule_id: Optional[str] = None
    status: str = "active"

class EmployeeUpdateSchema(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=120)
    department: Optional[str] = None
    position: Optional[str] = None
    employment_type: Optional[EmploymentType] = None
    contract: Optional[ContractSchema] = None
    manager_user_id: Optional[str] = None
    schedule_id: Optional[str] = None
    status: Optional[str] = None


class EmployeeCreateAccountSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    username: Optional[str] = None
    role: str = Field(default="employee")  # employee|manager|payroll_manager|admin