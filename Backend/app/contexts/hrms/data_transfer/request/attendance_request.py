from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class AttendanceCheckInSchema(BaseModel):
    employee_id: str
    check_in_time: datetime
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    wrong_location_reason: Optional[str] = None


class AttendanceCheckOutSchema(BaseModel):
    employee_id: str
    check_out_time: datetime
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)


class AttendanceApproveWrongLocationSchema(BaseModel):
    attendance_id: str
    admin_id: str
    approved: bool
    comment: Optional[str] = None


class AttendanceListQuerySchema(BaseModel):
    employee_id: Optional[str] = None
    status: Optional[str] = None
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=100)