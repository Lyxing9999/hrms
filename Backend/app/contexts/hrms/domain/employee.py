from __future__ import annotations
from enum import Enum
from datetime import date as date_type
from app.contexts.shared.lifecycle.domain import Lifecycle, now_utc
from app.contexts.hrms.errors.employee_exceptions import (
    ContractRequiredException,
    ContractDateInvalidException,
    EmployeeDeletedException,
)

class EmploymentType(str, Enum):
    PERMANENT = "permanent"
    CONTRACT = "contract"

class Employee:
    def __init__(
        self,
        *,
        employee_code: str,
        full_name: str,
        employment_type: EmploymentType | str,
        id: str | None = None,
        user_id: str | None = None,
        department: str | None = None,
        position: str | None = None,
        contract: dict | None = None,
        manager_user_id: str | None = None,
        schedule_id: str | None = None,
        status: str = "active",
        created_by: str | None = None,
        photo_url: str | None = None,
        lifecycle: Lifecycle | None = None,
    ) -> None:
        self.id = id  
        self.user_id = user_id

        self.employee_code = (employee_code or "").strip()
        self.full_name = (full_name or "").strip()

        self.employment_type = EmploymentType(str(employment_type).strip().lower())
        self.department = department
        self.position = position
        self.contract = contract or None

        self.manager_user_id = manager_user_id
        self.schedule_id = schedule_id
        self.status = status
        self.created_by = created_by
        self.photo_url = photo_url

        self.lifecycle = lifecycle or Lifecycle()
        self._validate_contract_rules()

    def _validate_contract_rules(self) -> None:
        if self.employment_type == EmploymentType.CONTRACT:
            if not self.contract:
                raise ContractRequiredException(self.id)
            s = self.contract.get("start_date")
            e = self.contract.get("end_date")
            if isinstance(s, str):
                s = date_type.fromisoformat(s)
            if isinstance(e, str):
                e = date_type.fromisoformat(e)
            if not s or not e or e < s:
                raise ContractDateInvalidException(s, e)

    def is_deleted(self) -> bool:
        return self.lifecycle.is_deleted()

    def link_user(self, user_id: str) -> None:
        if self.is_deleted():
            raise EmployeeDeletedException(self.id)
        self.user_id = str(user_id)
        self.lifecycle.touch(now_utc())


    def soft_delete(self, actor_id) -> Employee:
        return self.lifecycle.soft_delete(actor_id=actor_id)