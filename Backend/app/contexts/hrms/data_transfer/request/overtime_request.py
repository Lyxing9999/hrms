from __future__ import annotations

from datetime import datetime, date
from pydantic import BaseModel, Field, model_validator


class OvertimeCreateSchema(BaseModel):
    request_date: date
    start_time: datetime
    end_time: datetime
    reason: str = Field(..., min_length=3, max_length=500)

    @model_validator(mode="after")
    def validate_times(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self


class OvertimeApproveSchema(BaseModel):
    approved_hours: float | None = Field(default=None, ge=0)
    comment: str | None = Field(default=None, max_length=300)


class OvertimeRejectSchema(BaseModel):
    comment: str | None = Field(default=None, max_length=300)