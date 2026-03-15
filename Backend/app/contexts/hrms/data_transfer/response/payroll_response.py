from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.contexts.shared.lifecycle.dto import LifecycleDTO
from app.contexts.admin.data_transfer.responses.common import PaginatedDTO


class PayrollRunDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore", populate_by_name=True)

    id: str
    month: str
    generated_by: str
    status: str
    lifecycle: LifecycleDTO


class PayrollRunPaginatedDTO(PaginatedDTO[PayrollRunDTO]):
    pass


class PayslipDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore", populate_by_name=True)

    id: str
    payroll_run_id: str
    employee_id: str
    month: str
    base_salary: float
    payable_working_days: int
    paid_holiday_days: int
    unpaid_leave_days: int
    total_ot_hours: float
    ot_payment: float
    total_deductions: float
    net_salary: float
    status: str
    lifecycle: LifecycleDTO


class PayslipPaginatedDTO(PaginatedDTO[PayslipDTO]):
    pass