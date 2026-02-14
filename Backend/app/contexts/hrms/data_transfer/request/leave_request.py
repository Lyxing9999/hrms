# app/contexts/hrms/data_transfer/request/leave_request.py
from datetime import date
from pydantic import BaseModel, Field
from typing import Optional

class LeaveCreateSchema(BaseModel):
    employee_id: Optional[str] = None  # Can be provided or extracted from token
    leave_type: str = Field(..., description="annual|sick|unpaid|other")
    start_date: date
    end_date: date
    reason: str = Field(default="", max_length=500)


class LeaveUpdateSchema(BaseModel):
    leave_type: Optional[str] = Field(None, description="annual|sick|unpaid|other")
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    reason: Optional[str] = Field(None, max_length=500)


class LeaveReviewSchema(BaseModel):
    comment: Optional[str] = Field(default=None, max_length=500)
