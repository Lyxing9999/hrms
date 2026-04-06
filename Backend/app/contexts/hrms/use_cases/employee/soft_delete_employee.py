from __future__ import annotations

from app.contexts.shared.time_utils import utc_now


class SoftDeleteEmployeeUseCase:
    def __init__(self, *, employee_repository) -> None:
        self.employee_repository = employee_repository

    def execute(self, *, employee_id: str, actor_id):
        employee = self.employee_repository.find_by_id(employee_id)
        now = utc_now()

        return self.employee_repository.update_fields(
            employee["_id"],
            {
                "lifecycle.deleted_at": now,
                "lifecycle.deleted_by": actor_id,
                "lifecycle.updated_at": now,
            },
        )