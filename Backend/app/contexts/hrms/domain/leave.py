# app/contexts/hrms/domain/leave.py
from __future__ import annotations

from datetime import date as date_type
from enum import Enum
from bson import ObjectId

from app.contexts.shared.lifecycle.domain import Lifecycle, now_utc
from app.contexts.hrms.errors.leave_exceptions import (
    LeaveDateRangeInvalidException,
    LeaveOutsideContractException,
    LeaveAlreadyReviewedException,
    LeaveRequestDeletedException,
)

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
        employee_id: ObjectId | str,
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
        self.employee_id = employee_id if isinstance(employee_id, ObjectId) else ObjectId(employee_id)

        self.leave_type = LeaveType(str(leave_type).strip().lower())
        self.start_date = start_date
        self.end_date = end_date
        if self.end_date < self.start_date:
            raise LeaveDateRangeInvalidException(self.start_date, self.end_date)

        # contract boundary
        self.contract_start = contract_start
        self.contract_end = contract_end
        if not (self.contract_start <= self.start_date <= self.contract_end and
                self.contract_start <= self.end_date <= self.contract_end):
            raise LeaveOutsideContractException(self.start_date, self.end_date, self.contract_start, self.contract_end)

        self.reason = (reason or "").strip()
        self.status = LeaveStatus(str(status).strip().lower())
        self.is_paid = bool(is_paid)

        self.manager_user_id = manager_user_id
        self.manager_comment = manager_comment

        self.lifecycle = lifecycle or Lifecycle()

    def total_days(self) -> int:
        return (self.end_date - self.start_date).days + 1

    def approve(self, *, manager_id: ObjectId, comment: str | None = None) -> None:
        if self.is_deleted():
            raise LeaveRequestDeletedException(self.id)
        if self.status != LeaveStatus.PENDING:
            raise LeaveAlreadyReviewedException(self.id, self.status.value)

        self.status = LeaveStatus.APPROVED
        self.manager_user_id = manager_id
        self.manager_comment = comment
        self.lifecycle.touch(now_utc())

    def reject(self, *, manager_id: ObjectId, comment: str | None = None) -> None:
        if self.is_deleted():
            raise LeaveRequestDeletedException(self.id)
        if self.status != LeaveStatus.PENDING:
            raise LeaveAlreadyReviewedException(self.id, self.status.value)

        self.status = LeaveStatus.REJECTED
        self.manager_user_id = manager_id
        self.manager_comment = comment
        self.lifecycle.touch(now_utc())

    def cancel(self, *, actor_id: ObjectId) -> None:
        if self.is_deleted():
            raise LeaveRequestDeletedException(self.id)
        if self.status != LeaveStatus.PENDING:
            raise LeaveAlreadyReviewedException(self.id, self.status.value)

        self.status = LeaveStatus.CANCELLED
        self.lifecycle.touch(now_utc())

    def is_deleted(self) -> bool:
        return self.lifecycle.is_deleted()

    def soft_delete(self, *, actor_id: str | ObjectId) -> None:
        """Soft delete the leave request"""
        self.lifecycle.soft_delete(actor_id=str(actor_id))
