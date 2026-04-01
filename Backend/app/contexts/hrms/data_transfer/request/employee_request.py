from __future__ import annotations

from datetime import date
from typing import Optional, Literal

from pydantic import BaseModel, Field, EmailStr, model_validator


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

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_date < self.start_date:
            raise ValueError("end_date cannot be before start_date")
        return self


class EmployeeCreateSchema(BaseModel):
    employee_code: str = Field(..., min_length=2, max_length=30)
    full_name: str = Field(..., min_length=2, max_length=120)
    department: Optional[str] = None
    position: Optional[str] = None

    employment_type: EmploymentType = "contract"
    basic_salary: float = Field(..., ge=0)
    contract: Optional[ContractSchema] = None

    manager_user_id: Optional[str] = None
    schedule_id: Optional[str] = None
    work_location_id: str | None = None
    status: str = "active"
    photo_url: Optional[str] = None

    @model_validator(mode="after")
    def validate_contract_requirement(self):
        if self.employment_type == "contract" and self.contract is None:
            raise ValueError("contract is required when employment_type is 'contract'")
        return self


class EmployeeUpdateSchema(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=120)
    department: Optional[str] = None
    position: Optional[str] = None
    employment_type: Optional[EmploymentType] = None
    basic_salary: Optional[float] = Field(None, ge=0)
    work_location_id: str | None = None
    contract: Optional[ContractSchema] = None
    manager_user_id: Optional[str] = None
    schedule_id: Optional[str] = None
    status: Optional[str] = None
    photo_url: Optional[str] = None


class EmployeeCreateAccountSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    username: Optional[str] = None
    role: str = Field(default="employee")




class EmployeeAccountStatusSchema(BaseModel):
    status: str


class EmployeeLinkAccountSchema(BaseModel):
    user_id: str
    
class EmployeeAccountUpdateSchema(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None







class EmployeeAssignScheduleSchema(BaseModel):
    schedule_id: str


