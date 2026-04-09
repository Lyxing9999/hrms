from __future__ import annotations

from app.contexts.hrms.errors.schedule_exceptions import WorkingScheduleNotFoundException


class UpdateWorkingScheduleUseCase:
    def __init__(self, *, working_schedule_repository) -> None:
        self.working_schedule_repository = working_schedule_repository

    def execute(self, *, schedule_id, payload):
        schedule = self.working_schedule_repository.find_by_id(schedule_id)
        if not schedule:
            raise WorkingScheduleNotFoundException(schedule_id)

        if payload.name is not None:
            schedule.name = payload.name.strip()

        if payload.start_time is not None or payload.end_time is not None:
            start_time = payload.start_time or schedule.start_time
            end_time = payload.end_time or schedule.end_time
            schedule.update_times(start_time, end_time)

        if payload.working_days is not None:
            schedule.update_working_days(payload.working_days)

        if payload.is_default is True and not schedule.is_default:
            current_default = self.working_schedule_repository.find_default()
            if current_default and str(current_default.id) != str(schedule.id):
                current_default.is_default = False
                self.working_schedule_repository.save(current_default)
            schedule.set_as_default()

        return self.working_schedule_repository.save(schedule)