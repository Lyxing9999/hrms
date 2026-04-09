from __future__ import annotations

from datetime import date
from pydantic import BaseModel, Field


class LeaveSubmitSchema(BaseModel):
    leave_type: str = Field(..., min_length=1, max_length=50)
    start_date: date
    end_date: date
    reason: str = Field(..., min_length=3, max_length=500)


class LeaveApproveSchema(BaseModel):
    comment: str | None = Field(default=None, max_length=500)


class LeaveRejectSchema(BaseModel):
    comment: str | None = Field(default=None, max_length=500)