from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class LeaveCreateSchema(BaseModel):
    employee_id: str
    leave_type: str
    start_date: date
    end_date: date
    reason: str = Field(..., min_length=2, max_length=500)
    is_paid: bool = False

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_date < self.start_date:
            raise ValueError("end_date cannot be before start_date")
        return self


class LeaveApproveSchema(BaseModel):
    leave_request_id: str
    manager_id: str
    approved: bool
    comment: Optional[str] = None


class LeaveListQuerySchema(BaseModel):
    employee_id: Optional[str] = None
    manager_user_id: Optional[str] = None
    status: Optional[str] = None
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=100)