from __future__ import annotations

from datetime import datetime


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
        employee_id: str,
        check_in_time: datetime,
        latitude: float,
        longitude: float,
        wrong_location_reason: str | None = None,
    ) -> dict:
        employee = self._get_employee(employee_id)
        schedule = self._get_employee_schedule(employee)
        location = self._get_active_work_location()
        self._ensure_no_existing_attendance(employee, check_in_time)

        is_valid_location = self._is_valid_location(
            location=location,
            latitude=latitude,
            longitude=longitude,
        )

        attendance = self._build_attendance(
            employee=employee,
            schedule=schedule,
            location=location,
            check_in_time=check_in_time,
            latitude=latitude,
            longitude=longitude,
            is_valid_location=is_valid_location,
            wrong_location_reason=wrong_location_reason,
        )

        self._apply_late_rule(
            attendance=attendance,
            schedule=schedule,
            check_in_time=check_in_time,
        )

        self._save_attendance(attendance)
        self._write_audit_log(attendance=attendance, employee=employee)

        return self._build_result(attendance)

    def _get_employee(self, employee_id: str):
        # TODO: load employee from repository
        # TODO: raise exception if not found or inactive
        return self.employee_repository.get_by_id(employee_id)

    def _get_employee_schedule(self, employee):
        # TODO: validate employee has schedule_id
        # TODO: load schedule by employee.schedule_id
        return self.working_schedule_repository.get_by_id(employee.schedule_id)

    def _get_active_work_location(self):
        # TODO: change this to your actual repository method
        return self.work_location_repository.get_active_default()

    def _ensure_no_existing_attendance(self, employee, check_in_time: datetime) -> None:
        # TODO: check if attendance already exists for employee and date
        # TODO: raise domain/application exception if already checked in
        existing = self.attendance_repository.get_by_employee_and_date(
            employee.id,
            check_in_time.date(),
        )
        if existing is not None:
            raise ValueError("Attendance already exists for this date")

    def _is_valid_location(self, *, location, latitude: float, longitude: float) -> bool:
        # TODO: if you have multiple allowed locations, replace with matching logic
        return location.contains(latitude, longitude)

    def _build_attendance(
        self,
        *,
        employee,
        schedule,
        location,
        check_in_time: datetime,
        latitude: float,
        longitude: float,
        is_valid_location: bool,
        wrong_location_reason: str | None,
    ):
        # TODO: import Attendance from your domain
        # TODO: create Attendance with your real constructor fields
        attendance = None

        # TODO: call attendance.check_in(...)
        # example:
        # attendance.check_in(
        #     check_in_time=check_in_time,
        #     latitude=latitude,
        #     longitude=longitude,
        #     is_valid_location=is_valid_location,
        #     reason=wrong_location_reason,
        # )

        return attendance

    def _apply_late_rule(self, *, attendance, schedule, check_in_time: datetime) -> None:
        # TODO: compute schedule start datetime
        # TODO: calculate late minutes
        # TODO: call attendance.mark_late(late_minutes) if needed
        pass

    def _save_attendance(self, attendance) -> None:
        # TODO: use create/save/update based on your repository style
        self.attendance_repository.save(attendance)

    def _write_audit_log(self, *, attendance, employee) -> None:
        # TODO: write audit log if your project supports it
        if self.audit_log_repository is None:
            return

    def _build_result(self, attendance) -> dict:
        # TODO: customize response structure
        return {
            "attendance_id": str(attendance.id),
            "status": attendance.status.value,
            "late_minutes": attendance.late_minutes,
        }