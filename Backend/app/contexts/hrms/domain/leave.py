from __future__ import annotations

from datetime import date as date_type
from enum import Enum
from bson import ObjectId

from app.contexts.shared.lifecycle.domain import Lifecycle, now_utc


class LeaveType(str, Enum):
    ANNUAL = "annual"
    SICK = "sick"
    UNPAID = "unpaid"
    OTHER = "other"


class LeaveStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class LeaveRequest:
    def __init__(
        self,
        *,
        employee_id: ObjectId,
        leave_type: LeaveType | str,
        start_date: date_type,
        end_date: date_type,
        reason: str,
        contract_start: date_type,
        contract_end: date_type,
        is_paid: bool,
        id: ObjectId | None = None,
        status: LeaveStatus | str = LeaveStatus.PENDING,
        manager_user_id: ObjectId | None = None,
        manager_comment: str | None = None,
        lifecycle: Lifecycle | None = None,
    ) -> None:
        self.id = id or ObjectId()
        self.employee_id = employee_id
        self.leave_type = LeaveType(str(leave_type).strip().lower())
        self.start_date = start_date
        self.end_date = end_date
        self.reason = (reason or "").strip()
        self.contract_start = contract_start
        self.contract_end = contract_end
        self.is_paid = bool(is_paid)
        self.status = LeaveStatus(str(status).strip().lower())
        self.manager_user_id = manager_user_id
        self.manager_comment = (manager_comment or "").strip() or None
        self.lifecycle = lifecycle or Lifecycle()

        if self.end_date < self.start_date:
            raise ValueError("Leave end_date cannot be before start_date")
        if not self.reason:
            raise ValueError("Leave reason is required")
        if not (
            self.contract_start <= self.start_date <= self.contract_end
            and self.contract_start <= self.end_date <= self.contract_end
        ):
            raise ValueError("Leave request is outside contract period")

    def total_days(self) -> int:
        return (self.end_date - self.start_date).days + 1

    def approve(self, *, manager_id: ObjectId, comment: str | None = None) -> None:
        if self.status != LeaveStatus.PENDING:
            raise ValueError("Only pending leave request can be approved")
        self.status = LeaveStatus.APPROVED
        self.manager_user_id = manager_id
        self.manager_comment = (comment or "").strip() or None
        self.lifecycle.touch(now_utc())

    def reject(self, *, manager_id: ObjectId, comment: str | None = None) -> None:
        if self.status != LeaveStatus.PENDING:
            raise ValueError("Only pending leave request can be rejected")
        self.status = LeaveStatus.REJECTED
        self.manager_user_id = manager_id
        self.manager_comment = (comment or "").strip() or None
        self.lifecycle.touch(now_utc())

    def cancel(self, *, actor_id: ObjectId) -> None:
        if self.status != LeaveStatus.PENDING:
            raise ValueError("Only pending leave request can be cancelled")
        self.status = LeaveStatus.CANCELLED
        self.lifecycle.touch(now_utc())

    def is_deleted(self) -> bool:
        return self.lifecycle.is_deleted()

    def soft_delete(self, *, actor_id: ObjectId | str) -> None:
        self.lifecycle.soft_delete(actor_id=str(actor_id))