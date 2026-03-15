from __future__ import annotations

from datetime import datetime, timezone


class UpdateEmployeeUseCase:
    def __init__(self, *, employee_repository) -> None:
        self.employee_repository = employee_repository

    def execute(self, *, employee_id: str, payload, actor_id):
        employee = self.employee_repository.find_by_id(employee_id)

        update_data = payload.model_dump(exclude_unset=True)

        if "contract" in update_data and update_data["contract"] is not None:
            update_data["contract"] = payload.contract.model_dump()

        update_data["lifecycle.updated_at"] = datetime.now(timezone.utc)

        return self.employee_repository.update_fields(employee["_id"], update_data)