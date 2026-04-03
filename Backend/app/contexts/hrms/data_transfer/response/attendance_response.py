from __future__ import annotations

from datetime import datetime, date
from pydantic import BaseModel

from app.contexts.shared.lifecycle.dto import LifecycleDTO
from app.contexts.hrms.domain.attendance import Attendance

class AttendanceDTO(BaseModel):
    id: str
    employee_id: str | None = None
    attendance_date: date | datetime

    check_in_time: datetime | None = None
    check_out_time: datetime | None = None

    schedule_id: str | None = None
    location_id: str | None = None

    check_in_latitude: float | None = None
    check_in_longitude: float | None = None
    check_out_latitude: float | None = None
    check_out_longitude: float | None = None

    day_type: str
    is_ot_eligible: bool = False


    status: str
    notes: str | None = None
    late_minutes: int = 0
    early_leave_minutes: int = 0

    wrong_location_reason: str | None = None
    admin_comment: str | None = None
    location_reviewed_by: str | None = None

    lifecycle: LifecycleDTO

class AttendancePaginatedDTO(BaseModel):
    items: list[AttendanceDTO]
    total: int
    page: int
    page_size: int
    total_pages: int