from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class OvertimeCreateSchema(BaseModel):
    employee_id: str
    request_date: date
    start_time: datetime
    end_time: datetime
    reason: str = Field(..., min_length=2, max_length=500)

    @model_validator(mode="after")
    def validate_time_range(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self


class OvertimeApproveSchema(BaseModel):
    overtime_request_id: str
    manager_id: str
    approved_hours: Optional[float] = Field(None, ge=0)
    comment: Optional[str] = None


class OvertimeRejectSchema(BaseModel):
    overtime_request_id: str
    manager_id: str
    comment: Optional[str] = None


class OvertimeListQuerySchema(BaseModel):
    employee_id: Optional[str] = None
    manager_id: Optional[str] = None
    status: Optional[str] = None
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=100)