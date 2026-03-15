from __future__ import annotations

from enum import Enum
from datetime import datetime
from bson import ObjectId

from app.contexts.shared.lifecycle.domain import Lifecycle, now_utc


class AttendanceStatus(str, Enum):
    CHECKED_IN = "checked_in"
    CHECKED_OUT = "checked_out"
    LATE = "late"
    EARLY_LEAVE = "early_leave"
    ABSENT = "absent"
    HOLIDAY_OFF = "holiday_off"
    WEEKEND_OFF = "weekend_off"
    WRONG_LOCATION_PENDING = "wrong_location_pending"
    WRONG_LOCATION_APPROVED = "wrong_location_approved"
    WRONG_LOCATION_REJECTED = "wrong_location_rejected"


class Attendance:
    def __init__(
        self,
        *,
        employee_id: ObjectId,
        attendance_date: datetime,
        check_in_time: datetime | None = None,
        check_out_time: datetime | None = None,
        schedule_id: ObjectId | None = None,
        location_id: ObjectId | None = None,
        check_in_latitude: float | None = None,
        check_in_longitude: float | None = None,
        check_out_latitude: float | None = None,
        check_out_longitude: float | None = None,
        status: AttendanceStatus | str = AttendanceStatus.CHECKED_IN,
        notes: str | None = None,
        late_minutes: int = 0,
        early_leave_minutes: int = 0,
        wrong_location_reason: str | None = None,
        admin_comment: str | None = None,
        location_reviewed_by: ObjectId | None = None,
        id: ObjectId | None = None,
        lifecycle: Lifecycle | None = None,
    ) -> None:
        self.id = id or ObjectId()
        self.employee_id = employee_id
        self.attendance_date = attendance_date
        self.check_in_time = check_in_time
        self.check_out_time = check_out_time
        self.schedule_id = schedule_id
        self.location_id = location_id
        self.check_in_latitude = check_in_latitude
        self.check_in_longitude = check_in_longitude
        self.check_out_latitude = check_out_latitude
        self.check_out_longitude = check_out_longitude
        self.status = AttendanceStatus(str(status).strip().lower())
        self.notes = notes
        self.late_minutes = int(late_minutes)
        self.early_leave_minutes = int(early_leave_minutes)
        self.wrong_location_reason = (wrong_location_reason or "").strip() or None
        self.admin_comment = (admin_comment or "").strip() or None
        self.location_reviewed_by = location_reviewed_by
        self.lifecycle = lifecycle or Lifecycle()

    def check_in(
        self,
        *,
        check_in_time: datetime,
        latitude: float | None = None,
        longitude: float | None = None,
        is_valid_location: bool = True,
        reason: str | None = None,
    ) -> None:
        if self.check_in_time is not None:
            raise ValueError("Attendance already checked in")

        self.check_in_time = check_in_time
        self.check_in_latitude = latitude
        self.check_in_longitude = longitude

        if is_valid_location:
            self.status = AttendanceStatus.CHECKED_IN
        else:
            self.status = AttendanceStatus.WRONG_LOCATION_PENDING
            self.wrong_location_reason = (reason or "").strip() or None

        self.lifecycle.touch(now_utc())

    def check_out(
        self,
        *,
        check_out_time: datetime,
        latitude: float | None = None,
        longitude: float | None = None,
        early_leave_minutes: int = 0,
    ) -> None:
        if self.check_in_time is None:
            raise ValueError("Cannot check out before check in")
        if self.check_out_time is not None:
            raise ValueError("Attendance already checked out")
        if check_out_time < self.check_in_time:
            raise ValueError("Check-out time cannot be before check-in time")

        self.check_out_time = check_out_time
        self.check_out_latitude = latitude
        self.check_out_longitude = longitude
        self.early_leave_minutes = int(early_leave_minutes)

        if self.status == AttendanceStatus.WRONG_LOCATION_PENDING:
            # Keep pending until admin reviews.
            pass
        elif early_leave_minutes > 0:
            self.status = AttendanceStatus.EARLY_LEAVE
        elif self.late_minutes > 0:
            self.status = AttendanceStatus.LATE
        else:
            self.status = AttendanceStatus.CHECKED_OUT

        self.lifecycle.touch(now_utc())

    def mark_late(self, late_minutes: int) -> None:
        if late_minutes < 0:
            raise ValueError("late_minutes cannot be negative")
        self.late_minutes = int(late_minutes)
        if self.status not in {
            AttendanceStatus.WRONG_LOCATION_PENDING,
            AttendanceStatus.WRONG_LOCATION_APPROVED,
            AttendanceStatus.WRONG_LOCATION_REJECTED,
        } and late_minutes > 0:
            self.status = AttendanceStatus.LATE
        self.lifecycle.touch(now_utc())

    def approve_wrong_location(self, *, admin_id: ObjectId, comment: str | None = None) -> None:
        if self.status != AttendanceStatus.WRONG_LOCATION_PENDING:
            raise ValueError("Attendance is not waiting for wrong-location approval")
        self.status = AttendanceStatus.WRONG_LOCATION_APPROVED
        self.location_reviewed_by = admin_id
        self.admin_comment = (comment or "").strip() or None
        self.lifecycle.touch(now_utc())

    def reject_wrong_location(self, *, admin_id: ObjectId, comment: str | None = None) -> None:
        if self.status != AttendanceStatus.WRONG_LOCATION_PENDING:
            raise ValueError("Attendance is not waiting for wrong-location approval")
        self.status = AttendanceStatus.WRONG_LOCATION_REJECTED
        self.location_reviewed_by = admin_id
        self.admin_comment = (comment or "").strip() or None
        self.lifecycle.touch(now_utc())

    def mark_absent(self) -> None:
        self.status = AttendanceStatus.ABSENT
        self.lifecycle.touch(now_utc())

    def mark_holiday_off(self) -> None:
        self.status = AttendanceStatus.HOLIDAY_OFF
        self.lifecycle.touch(now_utc())

    def mark_weekend_off(self) -> None:
        self.status = AttendanceStatus.WEEKEND_OFF
        self.lifecycle.touch(now_utc())

    def total_working_hours(self) -> float:
        if not self.check_in_time or not self.check_out_time:
            return 0.0
        seconds = (self.check_out_time - self.check_in_time).total_seconds()
        return max(0.0, seconds / 3600.0)

    def is_deleted(self) -> bool:
        return self.lifecycle.is_deleted()

    def soft_delete(self, *, actor_id: ObjectId | str) -> None:
        self.lifecycle.soft_delete(actor_id=str(actor_id))