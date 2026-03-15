from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class GeneratePayrollSchema(BaseModel):
    month: str = Field(..., pattern=r"^\d{4}-\d{2}$")
    generated_by: str
    expected_working_days: int = Field(..., ge=1)


class PayrollFinalizeSchema(BaseModel):
    payroll_run_id: str
    actor_id: str


class PayrollMarkPaidSchema(BaseModel):
    payroll_run_id: str
    actor_id: str


class PayslipMarkPaidSchema(BaseModel):
    payslip_id: str
    actor_id: str


class PayrollRunListQuerySchema(BaseModel):
    status: Optional[str] = None
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=100)


class PayslipListQuerySchema(BaseModel):
    employee_id: Optional[str] = None
    payroll_run_id: Optional[str] = None
    month: Optional[str] = None
    status: Optional[str] = None
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=100)