from typing import List, Optional
from pydantic import BaseModel, RootModel, ConfigDict
from app.contexts.shared.lifecycle.dto import LifecycleDTO

class PayrollRunDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")

    id: str
    month: str
    status: str
    generated_by: str
    lifecycle: LifecycleDTO

class PayslipDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")

    id: str
    payroll_run_id: str
    employee_id: str
    month: str
    base_salary: float
    ot_payment: float
    deductions: float
    net_salary: float
    status: str
    lifecycle: LifecycleDTO

class PayslipDTOList(RootModel[List[PayslipDTO]]):
    pass