# app/contexts/hrms/data_transfer/response/working_schedule_response.py
from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import time as time_type

from app.contexts.shared.lifecycle.dto import LifecycleDTO
from app.contexts.admin.data_transfer.responses.common import PaginatedDTO


class WorkingScheduleDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore", populate_by_name=True)

    id: str
    name: str
    start_time: time_type
    end_time: time_type
    working_days: list[int]
    weekend_days: list[int]
    total_hours_per_day: float
    is_default: bool
    created_by: Optional[str] = None
    lifecycle: LifecycleDTO


class WorkingSchedulePaginatedDTO(PaginatedDTO[WorkingScheduleDTO]):
    pass
