from __future__ import annotations

from app.contexts.hrms.data_transfer.response.employee_response import EmployeeDTO
from app.contexts.shared.lifecycle.dto import LifecycleDTO


from app.contexts.shared.lifecycle.domain import now_utc

class EmployeeMapper:
    @staticmethod
    def to_dto(data: dict) -> EmployeeDTO:
        lifecycle = data.get("lifecycle") or {}
        created_at = lifecycle.get("created_at") or data.get("created_at") or now_utc()
        updated_at = lifecycle.get("updated_at") or data.get("updated_at") or created_at

        return EmployeeDTO(
            id=str(data["_id"]),
            user_id=str(data["user_id"]) if data.get("user_id") else None,
            employee_code=data.get("employee_code", ""),
            full_name=data.get("full_name", ""),
            department=data.get("department"),
            position=data.get("position"),
            employment_type=data.get("employment_type", ""),
            basic_salary=float(data.get("basic_salary", 0)),
            contract=data.get("contract"),
            manager_user_id=str(data["manager_user_id"]) if data.get("manager_user_id") else None,
            schedule_id=str(data["schedule_id"]) if data.get("schedule_id") else None,
            work_location_id=str(data["work_location_id"]) if data.get("work_location_id") else None,
            status=data.get("status", "active"),
            created_by=str(data["created_by"]) if data.get("created_by") else None,
            photo_url=data.get("photo_url"),
            lifecycle=LifecycleDTO(
                created_at=created_at,
                updated_at=updated_at,
                deleted_at=lifecycle.get("deleted_at"),
                deleted_by=str(lifecycle.get("deleted_by")) if lifecycle.get("deleted_by") else None,
            ),
        )