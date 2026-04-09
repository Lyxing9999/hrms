from __future__ import annotations

from datetime import date, datetime
from pydantic import BaseModel, ConfigDict



class AttendanceDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore", populate_by_name=True)

    id: str
    employee_id: str
    attendance_date: date

    check_in_time: datetime | None = None
    check_out_time: datetime | None = None

    schedule_id: str | None = None
    location_id: str | None = None

    check_in_latitude: float | None = None
    check_in_longitude: float | None = None
    check_out_latitude: float | None = None
    check_out_longitude: float | None = None

    day_type: str
    is_ot_eligible: bool
    status: str

    notes: str | None = None
    late_minutes: int = 0
    early_leave_minutes: int = 0

    wrong_location_reason: str | None = None
    late_reason: str | None = None
    early_leave_reason: str | None = None
    early_leave_review_status: str | None = None
    admin_comment: str | None = None

    location_reviewed_by: str | None = None
    early_leave_reviewed_by: str | None = None

    created_at: datetime | None = None
    updated_at: datetime | None = None

class PaginationDTO(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int


class AttendancePaginatedDTO(BaseModel):
    items: list[AttendanceDTO]
    pagination: PaginationDTO


class AttendanceTodayDTO(BaseModel):
    item: AttendanceDTO | None = None