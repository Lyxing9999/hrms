from __future__ import annotations

from enum import Enum
from datetime import date as date_type
from bson import ObjectId

from app.contexts.shared.lifecycle.domain import Lifecycle, now_utc


class EmploymentType(str, Enum):
    PERMANENT = "permanent"
    CONTRACT = "contract"


class EmployeeStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    TERMINATED = "terminated"


class Employee:
    def __init__(
        self,
        *,
        employee_code: str,
        full_name: str,
        employment_type: EmploymentType | str,
        basic_salary: float,
        department: str | None = None,
        position: str | None = None,
        user_id: ObjectId | None = None,
        manager_user_id: ObjectId | None = None,
        schedule_id: ObjectId | None = None,
        id: ObjectId | None = None,
        contract: dict | None = None,
        status: EmployeeStatus | str = EmployeeStatus.ACTIVE,
        photo_url: str | None = None,
        created_by: ObjectId | None = None,
        lifecycle: Lifecycle | None = None,
    ) -> None:
        self.id = id or ObjectId()
        self.employee_code = (employee_code or "").strip()
        self.full_name = (full_name or "").strip()
        self.employment_type = EmploymentType(str(employment_type).strip().lower())
        self.basic_salary = float(basic_salary)
        self.department = (department or "").strip() or None
        self.position = (position or "").strip() or None
        self.user_id = user_id
        self.manager_user_id = manager_user_id
        self.schedule_id = schedule_id
        self.contract = contract or None
        self.status = EmployeeStatus(str(status).strip().lower())
        self.photo_url = photo_url
        self.created_by = created_by
        self.lifecycle = lifecycle or Lifecycle()

        if not self.employee_code:
            raise ValueError("Employee code is required")
        if not self.full_name:
            raise ValueError("Employee full name is required")
        if self.basic_salary < 0:
            raise ValueError("Basic salary cannot be negative")

        self._validate_contract_rules()

    def _validate_contract_rules(self) -> None:
        if self.employment_type != EmploymentType.CONTRACT:
            return

        if not self.contract:
            raise ValueError("Contract info is required for contract employee")

        start_date = self.contract.get("start_date")
        end_date = self.contract.get("end_date")

        if isinstance(start_date, str):
            start_date = date_type.fromisoformat(start_date)
        if isinstance(end_date, str):
            end_date = date_type.fromisoformat(end_date)

        if not start_date or not end_date:
            raise ValueError("Contract start_date and end_date are required")
        if end_date < start_date:
            raise ValueError("Contract end_date cannot be before start_date")

    def assign_manager(self, manager_user_id: ObjectId) -> None:
        self.manager_user_id = manager_user_id
        self.lifecycle.touch(now_utc())

    def assign_schedule(self, schedule_id: ObjectId) -> None:
        self.schedule_id = schedule_id
        self.lifecycle.touch(now_utc())

    def link_user(self, user_id: ObjectId) -> None:
        if self.user_id is not None and self.user_id != user_id:
            raise ValueError("Employee already linked to another account")
        self.user_id = user_id
        self.lifecycle.touch(now_utc())

    def update_basic_salary(self, basic_salary: float) -> None:
        if basic_salary < 0:
            raise ValueError("Basic salary cannot be negative")
        self.basic_salary = float(basic_salary)
        self.lifecycle.touch(now_utc())

    def deactivate(self) -> None:
        self.status = EmployeeStatus.INACTIVE
        self.lifecycle.touch(now_utc())

    def activate(self) -> None:
        self.status = EmployeeStatus.ACTIVE
        self.lifecycle.touch(now_utc())

    def terminate(self) -> None:
        self.status = EmployeeStatus.TERMINATED
        self.lifecycle.touch(now_utc())

    def is_deleted(self) -> bool:
        return self.lifecycle.is_deleted()

    def soft_delete(self, *, actor_id: ObjectId | str) -> None:
        self.lifecycle.soft_delete(actor_id=str(actor_id))