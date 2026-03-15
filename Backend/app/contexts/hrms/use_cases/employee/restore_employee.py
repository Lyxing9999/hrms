from __future__ import annotations

from datetime import datetime, timezone


class RestoreEmployeeUseCase:
    def __init__(self, *, employee_repository) -> None:
        self.employee_repository = employee_repository

    def execute(self, *, employee_id: str):
        employee = self.employee_repository.find_by_id_including_deleted(employee_id)

        return self.employee_repository.update_fields(
            employee["_id"],
            {
                "lifecycle.deleted_at": None,
                "lifecycle.deleted_by": None,
                "lifecycle.updated_at": datetime.now(timezone.utc),
            },
        )