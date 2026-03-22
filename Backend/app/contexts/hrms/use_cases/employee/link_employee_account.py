from __future__ import annotations

from app.contexts.shared.model_converter import mongo_converter
from app.contexts.shared.lifecycle.domain import now_utc


class LinkEmployeeAccountUseCase:
    def __init__(self, *, employee_repository, iam_gateway) -> None:
        self.employee_repository = employee_repository
        self.iam_gateway = iam_gateway

    def execute(
        self,
        *,
        employee_id: str,
        user_id: str,
        actor_id: str,
    ):
        employee = self.employee_repository.find_by_id(employee_id)
        if not employee:
            raise ValueError("Employee not found")

        account = self.iam_gateway.get_account_summary_by_user_id(user_id)
        if not account:
            raise ValueError("Account not found")

        allowed_roles = {"employee", "manager", "payroll_manager"}
        role = str(account.get("role") or "").strip().lower()
        if role not in allowed_roles:
            raise ValueError("Account role is not allowed for HRMS employee link")

        existing = self.employee_repository.find_by_user_id(user_id)
        if existing and str(existing["_id"]) != str(employee["_id"]):
            raise ValueError("Account is already linked to another employee")

        updated = self.employee_repository.update_fields(
            employee_id,
            {
                "user_id": mongo_converter.convert_to_object_id(user_id),
                "lifecycle.updated_at": now_utc(),
            },
        )
        return updated