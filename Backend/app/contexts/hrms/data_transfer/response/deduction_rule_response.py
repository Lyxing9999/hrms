# app/contexts/hrms/data_transfer/response/deduction_rule_response.py
from typing import Optional
from pydantic import BaseModel, ConfigDict

from app.contexts.shared.lifecycle.dto import LifecycleDTO
from app.contexts.admin.data_transfer.responses.common import PaginatedDTO


class DeductionRuleDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore", populate_by_name=True)

    id: str
    type: str  # "late", "absent", "early_leave"
    min_minutes: int
    max_minutes: int
    deduction_percentage: float
    is_active: bool
    created_by: Optional[str] = None
    lifecycle: LifecycleDTO


class DeductionRulePaginatedDTO(PaginatedDTO[DeductionRuleDTO]):
    pass
