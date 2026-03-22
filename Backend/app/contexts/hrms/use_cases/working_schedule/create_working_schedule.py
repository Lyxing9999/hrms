from __future__ import annotations

from app.contexts.hrms.domain.working_schedule import WorkingSchedule


class CreateWorkingScheduleUseCase:
    def __init__(self, *, working_schedule_repository) -> None:
        self.working_schedule_repository = working_schedule_repository

    def execute(self, *, payload, created_by):
        if payload.is_default:
            existing_default = self.working_schedule_repository.find_default()
            if existing_default:
                existing_default.set_as_default()
                existing_default.is_default = False
                self.working_schedule_repository.save(existing_default)

        schedule = WorkingSchedule(
            name=payload.name,
            start_time=payload.start_time,
            end_time=payload.end_time,
            working_days=payload.working_days,
            weekend_days=payload.weekend_days,
            total_hours_per_day=payload.total_hours_per_day,
            is_default=payload.is_default,
            created_by=created_by,
        )

        return self.working_schedule_repository.save(schedule)