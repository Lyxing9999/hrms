# app/contexts/hrms/factories/attendance_factory.py
from bson import ObjectId
from datetime import datetime

from app.contexts.hrms.domain.attendance import Attendance, AttendanceStatus
from app.contexts.shared.lifecycle.domain import Lifecycle


class AttendanceFactory:
    @staticmethod
    def create_attendance(
        *,
        employee_id: ObjectId,
        check_in_time: datetime,
        location_id: ObjectId | None = None,
        check_in_latitude: float | None = None,
        check_in_longitude: float | None = None,
        notes: str | None = None,
        late_minutes: int = 0,
    ) -> Attendance:
        """Create a new attendance record"""
        status = AttendanceStatus.LATE if late_minutes > 0 else AttendanceStatus.CHECKED_IN
        
        return Attendance(
            employee_id=employee_id,
            check_in_time=check_in_time,
            location_id=location_id,
            check_in_latitude=check_in_latitude,
            check_in_longitude=check_in_longitude,
            notes=notes,
            late_minutes=late_minutes,
            status=status,
            lifecycle=Lifecycle(),
        )

    @staticmethod
    def from_dict(data: dict) -> Attendance:
        """Create attendance from dictionary"""
        lifecycle_data = data.get("lifecycle", {})
        lifecycle = Lifecycle(
            created_at=lifecycle_data.get("created_at"),
            updated_at=lifecycle_data.get("updated_at"),
            deleted_at=lifecycle_data.get("deleted_at"),
            deleted_by=lifecycle_data.get("deleted_by"),
        )

        return Attendance(
            id=data.get("_id"),
            employee_id=data["employee_id"],
            check_in_time=data["check_in_time"],
            check_out_time=data.get("check_out_time"),
            location_id=data.get("location_id"),
            check_in_latitude=data.get("check_in_latitude"),
            check_in_longitude=data.get("check_in_longitude"),
            check_out_latitude=data.get("check_out_latitude"),
            check_out_longitude=data.get("check_out_longitude"),
            status=data.get("status", AttendanceStatus.CHECKED_IN),
            notes=data.get("notes"),
            late_minutes=data.get("late_minutes", 0),
            early_leave_minutes=data.get("early_leave_minutes", 0),
            lifecycle=lifecycle,
        )
