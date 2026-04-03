from __future__ import annotations

from datetime import date, datetime
from pydantic import BaseModel

from app.contexts.shared.lifecycle.dto import LifecycleDTO
from app.contexts.admin.data_transfer.responses.common import PaginatedDTO


class OvertimeDTO(BaseModel):
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
    manager_id: str | None = None
    manager_comment: str | None = None
    approved_hours: float = 0.0
    calculated_payment: float = 0.0
    lifecycle: LifecycleDTO

class OvertimeRequestPaginatedDTO(PaginatedDTO[OvertimeDTO]):
    pass