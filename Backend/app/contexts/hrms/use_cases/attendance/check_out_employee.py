from __future__ import annotations

from datetime import datetime

from app.contexts.hrms.domain.audit_log import AuditLog
from app.contexts.hrms.domain.working_schedule import WorkingSchedule
from app.contexts.shared.time_utils import (
    ensure_utc,
    utc_now,
    to_cambodia,
    cambodia_start_of_day_as_utc,
)


class CheckOutEmployeeUseCase:
    def __init__(
        self,
        *,
        employee_repository,
        working_schedule_repository,
        attendance_repository,
        audit_log_repository=None,
    ) -> None:
        self.employee_repository = employee_repository
        self.working_schedule_repository = working_schedule_repository
        self.attendance_repository = attendance_repository
        self.audit_log_repository = audit_log_repository

    def execute(
        self,
        *,
        employee_id,
        check_out_time: datetime,
        latitude: float | None = None,
        longitude: float | None = None,
    ):
        employee = self._get_employee(employee_id)

        check_out_time_utc = ensure_utc(check_out_time)
        check_out_time_local = to_cambodia(check_out_time_utc)
        attendance_date_utc = cambodia_start_of_day_as_utc(check_out_time_utc)

        attendance = self._get_today_attendance(
            employee_id=employee["_id"],
            attendance_date=attendance_date_utc,
        )

        schedule = self._get_schedule(employee)

        if attendance.check_out_time is not None:
            raise ValueError("Employee already checked out")

        if attendance.check_in_time is None:
            raise ValueError("Attendance check-in not found for today")

        if check_out_time_utc < attendance.check_in_time:
            raise ValueError("Check-out time cannot be before check-in time")

        self._ensure_working_day(
            schedule=schedule,
            check_out_time_local=check_out_time_local,
        )

        early_leave_minutes = self._calculate_early_leave_minutes(
            schedule=schedule,
            check_out_time=check_out_time_utc,
        )

        attendance.check_out(
            check_out_time=check_out_time_utc,
            latitude=latitude,
            longitude=longitude,
        )

        attendance.early_leave_minutes = early_leave_minutes

        current_status = (
            attendance.status.value
            if hasattr(attendance.status, "value")
            else str(attendance.status)
        )

        if current_status == "wrong_location_pending":
            pass
        elif early_leave_minutes > 0:
            attendance.status = "early_leave"
        elif attendance.late_minutes > 0:
            attendance.status = "late"
        else:
            attendance.status = "checked_out"

        if hasattr(attendance.lifecycle, "touch"):
            attendance.lifecycle.touch(utc_now())
        else:
            attendance.lifecycle.updated_at = utc_now()

        attendance = self.attendance_repository.save(attendance)

        self._write_audit_log(
            action="attendance_check_out",
            actor_id=employee["_id"],
            entity_id=attendance.id,
            details={
                "status": attendance.status.value if hasattr(attendance.status, "value") else str(attendance.status),
                "early_leave_minutes": attendance.early_leave_minutes,
                "attendance_date": attendance.attendance_date.isoformat() if attendance.attendance_date else None,
                "check_out_time": attendance.check_out_time.isoformat() if attendance.check_out_time else None,
                "check_out_latitude": attendance.check_out_latitude,
                "check_out_longitude": attendance.check_out_longitude,
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

    def _get_today_attendance(self, *, employee_id, attendance_date):
        attendance = self.attendance_repository.find_by_employee_and_date(
            employee_id,
            attendance_date,
        )
        if not attendance:
            raise ValueError("Attendance check-in not found for today")
        return attendance

    def _get_schedule(self, employee: dict) -> WorkingSchedule:
        schedule_id = employee.get("schedule_id")
        if not schedule_id:
            raise ValueError("Employee has no assigned schedule")

        schedule = self.working_schedule_repository.find_by_id(schedule_id)
        if not schedule:
            raise ValueError("Working schedule not found")

        return schedule

    def _ensure_working_day(
        self,
        *,
        schedule: WorkingSchedule,
        check_out_time_local: datetime,
    ) -> None:
        weekday_value = check_out_time_local.weekday()
        if not schedule.is_working_day(weekday_value):
            raise ValueError("Today is not a scheduled working day")

    def _calculate_early_leave_minutes(
        self,
        *,
        schedule: WorkingSchedule,
        check_out_time: datetime,
    ) -> int:
        check_out_time_local = to_cambodia(check_out_time)
        end_time = schedule.end_time

        if not end_time:
            return 0

        if hasattr(end_time, "hour"):
            schedule_end = check_out_time_local.replace(
                hour=end_time.hour,
                minute=end_time.minute,
                second=getattr(end_time, "second", 0),
                microsecond=0,
            )
        else:
            hh, mm, *rest = str(end_time).split(":")
            ss = int(rest[0]) if rest else 0
            schedule_end = check_out_time_local.replace(
                hour=int(hh),
                minute=int(mm),
                second=ss,
                microsecond=0,
            )

        if check_out_time_local >= schedule_end:
            return 0

        return int((schedule_end - check_out_time_local).total_seconds() // 60)

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