from __future__ import annotations

from datetime import datetime

from app.contexts.hrms.domain.attendance import Attendance
from app.contexts.hrms.domain.audit_log import AuditLog
from app.contexts.hrms.domain.work_location import WorkLocation
from app.contexts.hrms.domain.working_schedule import WorkingSchedule
from app.contexts.shared.lifecycle.domain import Lifecycle
from app.contexts.shared.time_utils import (
    ensure_utc,
    utc_now,
    to_cambodia,
    cambodia_start_of_day_as_utc,
)


class CheckInEmployeeUseCase:
    def __init__(
        self,
        *,
        employee_repository,
        working_schedule_repository,
        work_location_repository,
        attendance_repository,
        audit_log_repository=None,
    ) -> None:
        self.employee_repository = employee_repository
        self.working_schedule_repository = working_schedule_repository
        self.work_location_repository = work_location_repository
        self.attendance_repository = attendance_repository
        self.audit_log_repository = audit_log_repository

    def execute(
        self,
        *,
        employee_id,
        check_in_time: datetime,
        latitude: float,
        longitude: float,
        wrong_location_reason: str | None = None,
    ) -> Attendance:
        employee = self._get_employee(employee_id)
        schedule = self._get_schedule(employee)
        location = self._get_work_location(employee)

        check_in_time_utc = ensure_utc(check_in_time)
        check_in_time_local = to_cambodia(check_in_time_utc)
        attendance_date_utc = cambodia_start_of_day_as_utc(check_in_time_utc)

        self._ensure_working_day(
            schedule=schedule,
            check_in_time_local=check_in_time_local,
        )

        self._ensure_not_checked_in(
            employee_id=employee["_id"],
            attendance_date=attendance_date_utc,
        )

        is_valid_location = self._is_valid_location(
            location=location,
            latitude=latitude,
            longitude=longitude,
        )

        if not is_valid_location and not wrong_location_reason:
            raise ValueError("wrong_location_reason is required when check-in location is invalid")

        late_minutes = self._calculate_late_minutes(
            schedule=schedule,
            check_in_time=check_in_time_utc,
        )

        now = utc_now()

        attendance = Attendance(
            employee_id=employee["_id"],
            attendance_date=attendance_date_utc,
            check_in_time=None,
            check_out_time=None,
            schedule_id=schedule.id if schedule else None,
            location_id=location.id if location else None,
            check_in_latitude=None,
            check_in_longitude=None,
            check_out_latitude=None,
            check_out_longitude=None,
            status="checked_in",
            notes=None,
            late_minutes=0,
            early_leave_minutes=0,
            wrong_location_reason=None,
            admin_comment=None,
            location_reviewed_by=None,
            lifecycle=Lifecycle(
                created_at=now,
                updated_at=now,
                deleted_at=None,
                deleted_by=None,
            ),
        )

        attendance.check_in(
            check_in_time=check_in_time_utc,
            latitude=latitude,
            longitude=longitude,
            is_valid_location=is_valid_location,
            reason=wrong_location_reason,
        )

        if late_minutes > 0:
            attendance.mark_late(late_minutes)

        attendance = self.attendance_repository.save(attendance)

        self._write_audit_log(
            action="attendance_check_in",
            actor_id=employee["_id"],
            entity_id=attendance.id,
            details={
                "status": attendance.status.value if hasattr(attendance.status, "value") else str(attendance.status),
                "late_minutes": attendance.late_minutes,
                "attendance_date": attendance.attendance_date.isoformat() if attendance.attendance_date else None,
                "check_in_time": attendance.check_in_time.isoformat() if attendance.check_in_time else None,
                "check_in_latitude": attendance.check_in_latitude,
                "check_in_longitude": attendance.check_in_longitude,
            },
        )

        return attendance

    def _get_employee(self, employee_id):
        employee = self.employee_repository.find_by_id(employee_id)
        if not employee:
            raise ValueError("Employee not found")
        if employee.get("status") != "active":
            raise ValueError("Employee is not active")
        return employee

    def _get_schedule(self, employee: dict) -> WorkingSchedule:
        schedule_id = employee.get("schedule_id")
        if not schedule_id:
            raise ValueError("Employee has no assigned schedule")

        schedule = self.working_schedule_repository.find_by_id(schedule_id)
        if not schedule:
            raise ValueError("Working schedule not found")

        return schedule
    def _get_work_location(self, employee: dict) -> WorkLocation | None:
        location_id = employee.get("work_location_id")
        if location_id:
            location = self.work_location_repository.find_by_id(location_id)
            if not location:
                raise ValueError("Assigned work location not found")
            if not location.is_active:
                raise ValueError("Assigned work location is inactive")
            return location

        return self._get_default_location()
    def _ensure_working_day(self, *, schedule: WorkingSchedule, check_in_time_local: datetime) -> None:
        weekday_value = check_in_time_local.weekday()
        if not schedule.is_working_day(weekday_value):
            raise ValueError("Today is not a scheduled working day")

    def _ensure_not_checked_in(self, *, employee_id, attendance_date) -> None:
        existing = self.attendance_repository.find_by_employee_and_date(
            employee_id,
            attendance_date,
        )
        if existing:
            raise ValueError("Attendance already exists for this date")

    def _is_valid_location(
        self,
        *,
        location: WorkLocation | None,
        latitude: float,
        longitude: float,
    ) -> bool:
        if not location:
            return True
        return location.contains(latitude, longitude)

    def _calculate_late_minutes(self, *, schedule: WorkingSchedule, check_in_time: datetime) -> int:
        check_in_time_local = to_cambodia(check_in_time)
        start_time = schedule.start_time

        if not start_time:
            return 0

        if hasattr(start_time, "hour"):
            schedule_start = check_in_time_local.replace(
                hour=start_time.hour,
                minute=start_time.minute,
                second=getattr(start_time, "second", 0),
                microsecond=0,
            )
        else:
            hh, mm, *rest = str(start_time).split(":")
            ss = int(rest[0]) if rest else 0
            schedule_start = check_in_time_local.replace(
                hour=int(hh),
                minute=int(mm),
                second=ss,
                microsecond=0,
            )

        if check_in_time_local <= schedule_start:
            return 0

        return int((check_in_time_local - schedule_start).total_seconds() // 60)

    def _write_audit_log(self, *, action: str, actor_id, entity_id, details: dict) -> None:
        if not self.audit_log_repository:
            return

        audit_log = AuditLog(
            id=None,
            entity_type="attendance",
            entity_id=entity_id,
            action=action,
            actor_id=actor_id,
            action_at=utc_now(),
            details=details,
        )

        self.audit_log_repository.save(audit_log)