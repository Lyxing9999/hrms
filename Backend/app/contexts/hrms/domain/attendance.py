# app/contexts/hrms/domain/attendance.py
from __future__ import annotations

from enum import Enum
from datetime import datetime
from bson import ObjectId
from app.contexts.shared.lifecycle.domain import Lifecycle, now_utc
from app.contexts.hrms.errors.attendance_exceptions import (
    AttendanceDeletedException,
    AttendanceAlreadyCheckedOutException,
    InvalidCheckOutTimeException,
)


class AttendanceStatus(str, Enum):
    CHECKED_IN = "checked_in"
    CHECKED_OUT = "checked_out"
    LATE = "late"
    EARLY_LEAVE = "early_leave"


class Attendance:
    def __init__(
        self,
        *,
        employee_id: ObjectId,
        check_in_time: datetime,
        location_id: ObjectId | None = None,
        check_in_latitude: float | None = None,
        check_in_longitude: float | None = None,
        id: ObjectId | None = None,
        check_out_time: datetime | None = None,
        check_out_latitude: float | None = None,
        check_out_longitude: float | None = None,
        status: AttendanceStatus | str = AttendanceStatus.CHECKED_IN,
        notes: str | None = None,
        late_minutes: int = 0,
        early_leave_minutes: int = 0,
        lifecycle: Lifecycle | None = None,
    ) -> None:
        self.id = id or ObjectId()
        self.employee_id = employee_id
        self.check_in_time = check_in_time
        self.check_out_time = check_out_time
        self.location_id = location_id
        self.check_in_latitude = check_in_latitude
        self.check_in_longitude = check_in_longitude
        self.check_out_latitude = check_out_latitude
        self.check_out_longitude = check_out_longitude
        
        # Handle status conversion - strip enum class prefix if present
        if isinstance(status, AttendanceStatus):
            self.status = status
        else:
            # Convert string to lowercase and remove any enum class prefix
            status_str = str(status).strip().lower()
            # Remove "attendancestatus." prefix if present
            if status_str.startswith("attendancestatus."):
                status_str = status_str.replace("attendancestatus.", "")
            self.status = AttendanceStatus(status_str)
        
        self.notes = notes
        self.late_minutes = late_minutes
        self.early_leave_minutes = early_leave_minutes
        self.lifecycle = lifecycle or Lifecycle()

    def check_out(
        self,
        *,
        check_out_time: datetime,
        latitude: float | None = None,
        longitude: float | None = None,
        early_leave_minutes: int = 0,
    ) -> None:
        if self.is_deleted():
            raise AttendanceDeletedException(self.id)
        
        if self.check_out_time is not None:
            raise AttendanceAlreadyCheckedOutException(self.id)
        
        if check_out_time < self.check_in_time:
            raise InvalidCheckOutTimeException(self.id)

        self.check_out_time = check_out_time
        self.check_out_latitude = latitude
        self.check_out_longitude = longitude
        self.early_leave_minutes = early_leave_minutes
        
        # Update status based on early leave
        if early_leave_minutes > 0:
            self.status = AttendanceStatus.EARLY_LEAVE
        else:
            self.status = AttendanceStatus.CHECKED_OUT
        
        self.lifecycle.touch(now_utc())

    def mark_late(self, late_minutes: int) -> None:
        self.late_minutes = late_minutes
        if late_minutes > 0:
            self.status = AttendanceStatus.LATE

    def is_deleted(self) -> bool:
        return self.lifecycle.is_deleted()

    def soft_delete(self, *, actor_id: ObjectId) -> None:
        self.lifecycle.soft_delete(now_utc(), actor_id)

    def restore(self) -> None:
        self.lifecycle.restore()
