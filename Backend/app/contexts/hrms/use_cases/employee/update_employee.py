from __future__ import annotations

from datetime import datetime, timezone

from app.contexts.shared.model_converter import mongo_converter


class UpdateEmployeeUseCase:
    def __init__(self, *, employee_repository) -> None:
        self.employee_repository = employee_repository

    def execute(self, *, employee_id: str, payload, actor_id):
        employee = self.employee_repository.find_by_id(employee_id)

        update_data = payload.model_dump(exclude_unset=True)

        if "contract" in update_data and update_data["contract"] is not None:
            # Use JSON mode so date fields are serialized to ISO strings.
            update_data["contract"] = payload.contract.model_dump(mode="json")

        if "schedule_id" in update_data:
            update_data["schedule_id"] = mongo_converter.convert_to_object_id(
                update_data["schedule_id"]
            )

        if "work_location_id" in update_data:
            update_data["work_location_id"] = mongo_converter.convert_to_object_id(
                update_data["work_location_id"]
            )

        if "manager_user_id" in update_data:
            update_data["manager_user_id"] = mongo_converter.convert_to_object_id(
                update_data["manager_user_id"]
            )

        update_data["lifecycle.updated_at"] = datetime.now(timezone.utc)

        return self.employee_repository.update_fields(employee["_id"], update_data)