from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.contexts.shared.lifecycle.dto import LifecycleDTO


class DeductionRuleDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore", populate_by_name=True)

    id: str
    type: str
    min_minutes: int
    max_minutes: Optional[int] = None
    deduction_percentage: float
    is_active: bool
    created_by: Optional[str] = None
    lifecycle: LifecycleDTO