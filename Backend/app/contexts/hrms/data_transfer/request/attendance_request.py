# app/contexts/hrms/data_transfer/request/attendance_request.py
from pydantic import BaseModel, Field
from datetime import datetime


class AttendanceCheckInSchema(BaseModel):
    employee_id: str | None = Field(None, description="Employee ID (optional, extracted from token)")
    location_id: str | None = Field(None, description="Work location ID")
    latitude: float | None = Field(None, ge=-90, le=90, description="Check-in latitude")
    longitude: float | None = Field(None, ge=-180, le=180, description="Check-in longitude")
    notes: str | None = Field(None, max_length=500, description="Optional notes")


class AttendanceCheckOutSchema(BaseModel):
    latitude: float | None = Field(None, ge=-90, le=90, description="Check-out latitude")
    longitude: float | None = Field(None, ge=-180, le=180, description="Check-out longitude")
    notes: str | None = Field(None, max_length=500, description="Optional notes")


class AttendanceUpdateSchema(BaseModel):
    check_in_time: datetime | None = None
    check_out_time: datetime | None = None
    location_id: str | None = None
    notes: str | None = Field(None, max_length=500)
    late_minutes: int | None = Field(None, ge=0)
    early_leave_minutes: int | None = Field(None, ge=0)
