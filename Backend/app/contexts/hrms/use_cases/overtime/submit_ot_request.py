from __future__ import annotations

from datetime import date as date_type, datetime


class SubmitOtRequestUseCase:
    def __init__(
        self,
        *,
        employee_repository,
        working_schedule_repository,
        public_holiday_repository,
        overtime_repository,
        audit_log_repository=None,
    ) -> None:
        self.employee_repository = employee_repository
        self.working_schedule_repository = working_schedule_repository
        self.public_holiday_repository = public_holiday_repository
        self.overtime_repository = overtime_repository
        self.audit_log_repository = audit_log_repository

    def execute(
        self,
        *,
        employee_id: str,
        request_date: date_type,
        start_time: datetime,
        end_time: datetime,
        reason: str,
    ) -> dict:
        employee = self._get_employee(employee_id)
        schedule = self._get_schedule(employee)
        day_type = self._determine_day_type(
            schedule=schedule,
            request_date=request_date,
        )
        schedule_end_time = self._build_schedule_end_time(
            request_date=request_date,
            schedule=schedule,
        )

        self._ensure_no_duplicate_request(
            employee=employee,
            request_date=request_date,
            start_time=start_time,
            end_time=end_time,
        )

        overtime_request = self._build_overtime_request(
            employee=employee,
            request_date=request_date,
            start_time=start_time,
            end_time=end_time,
            schedule_end_time=schedule_end_time,
            reason=reason,
            day_type=day_type,
        )

        self._save_overtime_request(overtime_request)
        self._write_audit_log(overtime_request=overtime_request, employee=employee)

        return self._build_result(overtime_request)

    def _get_employee(self, employee_id: str):
        # TODO
        return self.employee_repository.get_by_id(employee_id)

    def _get_schedule(self, employee):
        # TODO
        return self.working_schedule_repository.get_by_id(employee.schedule_id)

    def _determine_day_type(self, *, schedule, request_date: date_type):
        # TODO: use holiday + weekend + working day logic
        # TODO: return your OvertimeDayType enum
        holiday = self.public_holiday_repository.get_by_date(request_date)
        if holiday is not None:
            return "public_holiday"
        if schedule.is_weekend(request_date.weekday()):
            return "weekend"
        return "working_day"

    def _build_schedule_end_time(self, *, request_date: date_type, schedule):
        # TODO: build datetime from request_date + schedule.end_time
        return datetime.combine(request_date, schedule.end_time)

    def _ensure_no_duplicate_request(
        self,
        *,
        employee,
        request_date: date_type,
        start_time: datetime,
        end_time: datetime,
    ) -> None:
        # TODO: optional rule if your system disallows duplicate OT requests for same period
        pass

    def _build_overtime_request(
        self,
        *,
        employee,
        request_date: date_type,
        start_time: datetime,
        end_time: datetime,
        schedule_end_time,
        reason: str,
        day_type,
    ):
        # TODO: import and create OvertimeRequest
        overtime_request = None

        # example:
        # overtime_request = OvertimeRequest(
        #     employee_id=employee.id,
        #     request_date=request_date,
        #     start_time=start_time,
        #     end_time=end_time,
        #     schedule_end_time=schedule_end_time,
        #     reason=reason,
        #     day_type=day_type,
        #     basic_salary=employee.basic_salary,
        # )

        return overtime_request

    def _save_overtime_request(self, overtime_request) -> None:
        # TODO
        self.overtime_repository.save(overtime_request)

    def _write_audit_log(self, *, overtime_request, employee) -> None:
        # TODO
        if self.audit_log_repository is None:
            return

    def _build_result(self, overtime_request) -> dict:
        return {
            "overtime_request_id": str(overtime_request.id),
            "status": overtime_request.status.value,
            "requested_hours": overtime_request.requested_hours(),
        }