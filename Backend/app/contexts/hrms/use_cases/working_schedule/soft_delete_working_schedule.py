from __future__ import annotations

from app.contexts.hrms.errors.schedule_exceptions import (
    DefaultWorkingScheduleDeletionNotAllowedException,
    WorkingScheduleNotFoundException,
)


class SoftDeleteWorkingScheduleUseCase:
    def __init__(self, *, working_schedule_repository) -> None:
        self.working_schedule_repository = working_schedule_repository

    def execute(self, *, schedule_id, actor_id):
        schedule = self.working_schedule_repository.find_by_id(schedule_id)
        if not schedule:
            raise WorkingScheduleNotFoundException(schedule_id)

        if schedule.is_default:
            raise DefaultWorkingScheduleDeletionNotAllowedException(schedule_id)

        schedule.soft_delete(actor_id=actor_id)
        return self.working_schedule_repository.save(schedule)