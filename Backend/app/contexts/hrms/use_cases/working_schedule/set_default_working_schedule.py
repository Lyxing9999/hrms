from __future__ import annotations

from app.contexts.hrms.errors.schedule_exceptions import WorkingScheduleNotFoundException


class SetDefaultWorkingScheduleUseCase:
    def __init__(self, *, working_schedule_repository) -> None:
        self.working_schedule_repository = working_schedule_repository

    def execute(self, *, schedule_id):
        schedule = self.working_schedule_repository.find_by_id(schedule_id)
        if not schedule:
            raise WorkingScheduleNotFoundException(schedule_id)

        current_default = self.working_schedule_repository.find_default()
        if current_default and str(current_default.id) != str(schedule.id):
            current_default.is_default = False
            self.working_schedule_repository.save(current_default)

        schedule.set_as_default()
        return self.working_schedule_repository.save(schedule)