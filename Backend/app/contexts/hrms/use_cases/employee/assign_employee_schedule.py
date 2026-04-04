from __future__ import annotations

from app.contexts.hrms.errors.schedule_exceptions import (
    WorkingScheduleDeletedException,
    WorkingScheduleNotFoundException,
)
from app.contexts.shared.lifecycle.domain import now_utc


class AssignEmployeeScheduleUseCase:
    def __init__(
        self,
        *,
        employee_repository,
        working_schedule_repository,
    ) -> None:
        self.employee_repository = employee_repository
        self.working_schedule_repository = working_schedule_repository

    def execute(
        self,
        *,
        employee_id: str,
        schedule_id: str,
        actor_id: str,
    ) -> dict:
        employee = self.employee_repository.find_by_id(employee_id)
        schedule = self.working_schedule_repository.find_by_id(schedule_id)

        if not schedule:
            raise WorkingScheduleNotFoundException(schedule_id)

        if schedule.is_deleted():
            raise WorkingScheduleDeletedException(schedule_id)

        updated_employee = self.employee_repository.update_fields(
            employee_id,
            {
                "schedule_id": schedule.id,
                "lifecycle.updated_at": now_utc(),
            },
        )

        return updated_employee