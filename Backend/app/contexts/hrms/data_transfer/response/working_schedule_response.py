from __future__ import annotations

from datetime import time
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.contexts.shared.lifecycle.dto import LifecycleDTO


class WorkingScheduleDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore", populate_by_name=True)

    id: str
    name: str
    start_time: time
    end_time: time
    working_days: list[int]
    weekend_days: list[int]
    total_hours_per_day: float
    is_default: bool
    created_by: Optional[str] = None
    lifecycle: LifecycleDTO