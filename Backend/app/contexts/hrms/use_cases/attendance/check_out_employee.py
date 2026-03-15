from __future__ import annotations

from datetime import datetime


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
        employee_id: str,
        check_out_time: datetime,
        latitude: float | None = None,
        longitude: float | None = None,
    ) -> dict:
        employee = self._get_employee(employee_id)
        attendance = self._get_today_attendance(employee, check_out_time)
        schedule = self._get_schedule_for_attendance(employee)

        early_leave_minutes = self._calculate_early_leave_minutes(
            schedule=schedule,
            check_out_time=check_out_time,
        )

        self._perform_check_out(
            attendance=attendance,
            check_out_time=check_out_time,
            latitude=latitude,
            longitude=longitude,
            early_leave_minutes=early_leave_minutes,
        )

        self._save_attendance(attendance)
        self._write_audit_log(attendance=attendance, employee=employee)

        return self._build_result(attendance)

    def _get_employee(self, employee_id: str):
        # TODO
        return self.employee_repository.get_by_id(employee_id)

    def _get_today_attendance(self, employee, check_out_time: datetime):
        # TODO: load attendance for employee + date
        # TODO: ensure attendance exists and not already checked out
        return self.attendance_repository.get_by_employee_and_date(
            employee.id,
            check_out_time.date(),
        )

    def _get_schedule_for_attendance(self, employee):
        # TODO
        return self.working_schedule_repository.get_by_id(employee.schedule_id)

    def _calculate_early_leave_minutes(self, *, schedule, check_out_time: datetime) -> int:
        # TODO: build end-of-work datetime from schedule.end_time
        # TODO: calculate early leave minutes
        return 0

    def _perform_check_out(
        self,
        *,
        attendance,
        check_out_time: datetime,
        latitude: float | None,
        longitude: float | None,
        early_leave_minutes: int,
    ) -> None:
        # TODO: call attendance.check_out(...)
        attendance.check_out(
            check_out_time=check_out_time,
            latitude=latitude,
            longitude=longitude,
            early_leave_minutes=early_leave_minutes,
        )

    def _save_attendance(self, attendance) -> None:
        # TODO
        self.attendance_repository.save(attendance)

    def _write_audit_log(self, *, attendance, employee) -> None:
        # TODO
        if self.audit_log_repository is None:
            return

    def _build_result(self, attendance) -> dict:
        return {
            "attendance_id": str(attendance.id),
            "status": attendance.status.value,
            "early_leave_minutes": attendance.early_leave_minutes,
            "total_working_hours": attendance.total_working_hours(),
        }