from __future__ import annotations

from app.contexts.hrms.domain.overtime import (
    OvertimeRequest,
    OvertimeDayType,
)


class CreateOvertimeRequestUseCase:
    def __init__(
        self,
        *,
        employee_repository,
        working_schedule_repository,
        public_holiday_repository,
        overtime_repository,
    ) -> None:
        self.employee_repository = employee_repository
        self.working_schedule_repository = working_schedule_repository
        self.public_holiday_repository = public_holiday_repository
        self.overtime_repository = overtime_repository

    def execute(self, *, employee_id, payload):
        employee = self.employee_repository.find_by_id(employee_id)
        if not employee:
            raise ValueError("Employee not found")

        if str(employee.get("status") or "inactive") != "active":
            raise ValueError("Employee is not active")

        schedule_id = employee.get("schedule_id")
        if not schedule_id:
            raise ValueError("Employee has no assigned schedule")

        schedule = self.working_schedule_repository.find_by_id(schedule_id)
        if not schedule:
            raise ValueError("Working schedule not found")

        day_type = self._resolve_day_type(
            request_date=payload.request_date,
            schedule=schedule,
        )

        schedule_end_time = payload.start_time.replace(
            hour=schedule.end_time.hour,
            minute=schedule.end_time.minute,
            second=getattr(schedule.end_time, "second", 0),
            microsecond=0,
        )

        if day_type == OvertimeDayType.WORKING_DAY and payload.start_time < schedule_end_time:
            raise ValueError("Working day overtime must start after scheduled end time")

        overlap = self.overtime_repository.find_overlapping_request(
            employee_id=employee["_id"],
            request_date=payload.request_date,
            start_time=payload.start_time,
            end_time=payload.end_time,
        )
        if overlap:
            raise ValueError("Overlapping overtime request already exists")

        ot = OvertimeRequest(
            employee_id=employee["_id"],
            request_date=payload.request_date,
            start_time=payload.start_time,
            end_time=payload.end_time,
            schedule_end_time=schedule_end_time,
            reason=payload.reason,
            day_type=day_type,
            basic_salary=float(employee.get("basic_salary") or 0),
        )

        return self.overtime_repository.save(ot)

    def _resolve_day_type(self, *, request_date, schedule):
        holiday = self.public_holiday_repository.find_by_date(request_date)
        if holiday and not holiday.is_deleted():
            return OvertimeDayType.PUBLIC_HOLIDAY

        if schedule.is_weekend(request_date.weekday()):
            return OvertimeDayType.WEEKEND

        return OvertimeDayType.WORKING_DAY