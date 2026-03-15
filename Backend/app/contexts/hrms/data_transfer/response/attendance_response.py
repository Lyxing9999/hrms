from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.contexts.shared.lifecycle.dto import LifecycleDTO
from app.contexts.admin.data_transfer.responses.common import PaginatedDTO


class AttendanceDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore", populate_by_name=True)

    id: str
    employee_id: str
    attendance_date: datetime

    check_in_time: Optional[datetime] = None
    check_out_time: Optional[datetime] = None

    schedule_id: Optional[str] = None
    location_id: Optional[str] = None

    check_in_latitude: Optional[float] = None
    check_in_longitude: Optional[float] = None
    check_out_latitude: Optional[float] = None
    check_out_longitude: Optional[float] = None

    status: str
    notes: Optional[str] = None
    late_minutes: int = 0
    early_leave_minutes: int = 0

    wrong_location_reason: Optional[str] = None
    admin_comment: Optional[str] = None
    location_reviewed_by: Optional[str] = None

    lifecycle: LifecycleDTO


class AttendancePaginatedDTO(PaginatedDTO[AttendanceDTO]):
    pass