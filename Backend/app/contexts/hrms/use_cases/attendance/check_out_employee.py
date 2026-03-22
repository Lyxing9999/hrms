from __future__ import annotations

from datetime import datetime, timezone


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
    ) -> dict:
        employee = self._get_employee(employee_id)
        attendance = self._get_today_attendance(employee_id=employee["_id"], attendance_date=check_out_time.date())
        schedule = self._get_schedule(employee)

        if attendance.get("check_out_time") is not None:
            raise ValueError("Employee already checked out")

        if check_out_time < attendance["check_in_time"]:
            raise ValueError("Check-out time cannot be before check-in time")

        early_leave_minutes = self._calculate_early_leave_minutes(
            schedule=schedule,
            check_out_time=check_out_time,
        )

        new_status = attendance.get("status", "checked_in")
        if new_status == "wrong_location_pending":
            # keep pending until admin reviews
            pass
        elif early_leave_minutes > 0:
            new_status = "early_leave"
        elif attendance.get("late_minutes", 0) > 0:
            new_status = "late"
        else:
            new_status = "checked_out"

        updated = self.attendance_repository.update_fields(
            attendance["_id"],
            {
                "check_out_time": check_out_time,
                "check_out_latitude": latitude,
                "check_out_longitude": longitude,
                "early_leave_minutes": early_leave_minutes,
                "status": new_status,
                "lifecycle.updated_at": datetime.now(timezone.utc),
            },
        )

        self._write_audit_log(
            action="attendance_check_out",
            actor_id=employee["_id"],
            entity_id=updated["_id"],
            details={
                "status": updated["status"],
                "early_leave_minutes": updated.get("early_leave_minutes", 0),
                "attendance_date": str(updated["attendance_date"]),
            },
        )

        return updated

    def _get_employee(self, employee_id):
        employee = self.employee_repository.find_by_id(employee_id)
        if not employee:
            raise ValueError("Employee not found")
        if employee.get("status") != "active":
            raise ValueError("Employee is not active")
        return employee

    def _get_today_attendance(self, *, employee_id, attendance_date):
        attendance = self.attendance_repository.find_by_employee_and_date(employee_id, attendance_date)
        if not attendance:
            raise ValueError("Attendance check-in not found for today")
        return attendance

    def _get_schedule(self, employee: dict) -> dict:
        schedule_id = employee.get("schedule_id")
        if not schedule_id:
            raise ValueError("Employee has no assigned schedule")
        schedule = self.working_schedule_repository.find_by_id(schedule_id)
        if not schedule:
            raise ValueError("Working schedule not found")
        return schedule

    def _calculate_early_leave_minutes(self, *, schedule: dict, check_out_time: datetime) -> int:
        end_time = schedule.get("end_time")
        if not end_time:
            return 0

        if hasattr(end_time, "hour"):
            schedule_end = check_out_time.replace(
                hour=end_time.hour,
                minute=end_time.minute,
                second=getattr(end_time, "second", 0),
                microsecond=0,
            )
        else:
            hh, mm, *rest = str(end_time).split(":")
            ss = int(rest[0]) if rest else 0
            schedule_end = check_out_time.replace(
                hour=int(hh),
                minute=int(mm),
                second=ss,
                microsecond=0,
            )

        if check_out_time >= schedule_end:
            return 0

        return int((schedule_end - check_out_time).total_seconds() // 60)

    def _write_audit_log(self, *, action: str, actor_id, entity_id, details: dict) -> None:
        if not self.audit_log_repository:
            return

        self.audit_log_repository.save(
            {
                "entity_type": "attendance",
                "entity_id": entity_id,
                "action": action,
                "actor_id": actor_id,
                "action_at": datetime.now(timezone.utc),
                "details": details,
            }
        )