from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.contexts.shared.lifecycle.dto import LifecycleDTO
from app.contexts.admin.data_transfer.responses.common import PaginatedDTO


class OvertimeRequestDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore", populate_by_name=True)

    id: str
    employee_id: str
    request_date: date
    start_time: datetime
    end_time: datetime
    schedule_end_time: datetime
    reason: str
    day_type: str
    basic_salary: float
    submitted_at: datetime
    status: str
    manager_id: Optional[str] = None
    manager_comment: Optional[str] = None
    approved_hours: float = 0
    calculated_payment: float = 0
    lifecycle: LifecycleDTO


class OvertimeRequestPaginatedDTO(PaginatedDTO[OvertimeRequestDTO]):
    pass