from __future__ import annotations

from app.contexts.hrms.errors.schedule_exceptions import WorkingScheduleNotFoundException


class RestoreWorkingScheduleUseCase:
    def __init__(self, *, working_schedule_repository) -> None:
        self.working_schedule_repository = working_schedule_repository

    def execute(self, *, schedule_id):
        schedule = self.working_schedule_repository.find_by_id(schedule_id)
        if not schedule:
            raise WorkingScheduleNotFoundException(schedule_id)

        schedule.lifecycle.restore()
        return self.working_schedule_repository.save(schedule)
