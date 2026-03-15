from __future__ import annotations

from datetime import time
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class WorkingScheduleCreateSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    start_time: time
    end_time: time
    working_days: list[int] = Field(..., min_length=1)
    weekend_days: Optional[list[int]] = None
    total_hours_per_day: Optional[float] = Field(None, gt=0)
    is_default: bool = False

    @model_validator(mode="after")
    def validate_schedule(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        if not all(0 <= d <= 6 for d in self.working_days):
            raise ValueError("working_days must be between 0 and 6")
        return self


class WorkingScheduleUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    working_days: Optional[list[int]] = None
    weekend_days: Optional[list[int]] = None
    total_hours_per_day: Optional[float] = Field(None, gt=0)
    is_default: Optional[bool] = None