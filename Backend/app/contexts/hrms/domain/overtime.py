from __future__ import annotations

from enum import Enum
from datetime import datetime, date as date_type, timedelta
from bson import ObjectId

from app.contexts.shared.lifecycle.domain import Lifecycle, now_utc


class OvertimeStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class OvertimeDayType(str, Enum):
    WORKING_DAY = "working_day"
    WEEKEND = "weekend"
    PUBLIC_HOLIDAY = "public_holiday"


class OvertimeRequest:
    WORKING_DAY_RATE = 1.5
    HOLIDAY_OR_WEEKEND_RATE = 2.0
    MIN_SUBMISSION_HOURS_BEFORE_SCHEDULE_END = 3

    @staticmethod
    def _normalize_day_type(value) -> OvertimeDayType:
        if isinstance(value, OvertimeDayType):
            return value
        return OvertimeDayType(str(value).strip().lower())

    @staticmethod
    def _normalize_status(value) -> OvertimeStatus:
        if isinstance(value, OvertimeStatus):
            return value
        return OvertimeStatus(str(value).strip().lower())

    def __init__(
        self,
        *,
        employee_id: ObjectId,
        request_date: date_type,
        start_time: datetime,
        end_time: datetime,
        schedule_end_time: datetime,
        reason: str,
        day_type: OvertimeDayType | str,
        basic_salary: float,
        id: ObjectId | None = None,
        submitted_at: datetime | None = None,
        status: OvertimeStatus | str = OvertimeStatus.PENDING,
        manager_id: ObjectId | None = None,
        manager_comment: str | None = None,
        approved_hours: float = 0.0,
        calculated_payment: float = 0.0,
        lifecycle: Lifecycle | None = None,
    ) -> None:
        self.id = id or ObjectId()
        self.employee_id = employee_id
        self.request_date = request_date
        self.start_time = start_time
        self.end_time = end_time
        self.schedule_end_time = schedule_end_time
        self.reason = (reason or "").strip()
        self.day_type = self._normalize_day_type(day_type)
        self.basic_salary = float(basic_salary)
        self.submitted_at = submitted_at or now_utc()
        self.status = self._normalize_status(status)
        self.manager_id = manager_id
        self.manager_comment = (manager_comment or "").strip() or None
        self.approved_hours = float(approved_hours)
        self.calculated_payment = float(calculated_payment)
        self.lifecycle = lifecycle or Lifecycle()

        self._validate_initial_state()

    def _validate_initial_state(self) -> None:
        if self.end_time <= self.start_time:
            raise ValueError("OT end_time must be after start_time")

        if not self.reason:
            raise ValueError("OT reason is required")

        if self.basic_salary < 0:
            raise ValueError("Basic salary cannot be negative")

        self._validate_submission_deadline()

    def _validate_submission_deadline(self) -> None:
        latest_submit_time = self.schedule_end_time - timedelta(
            hours=self.MIN_SUBMISSION_HOURS_BEFORE_SCHEDULE_END
        )
        if self.submitted_at > latest_submit_time:
            raise ValueError("OT request must be submitted at least 3 hours before end of working time")

    def requested_hours(self) -> float:
        return (self.end_time - self.start_time).total_seconds() / 3600.0

    def ot_rate_multiplier(self) -> float:
        if self.day_type == OvertimeDayType.WORKING_DAY:
            return self.WORKING_DAY_RATE
        return self.HOLIDAY_OR_WEEKEND_RATE

    def calculate_payment(self, hours: float | None = None) -> float:
        actual_hours = self.requested_hours() if hours is None else float(hours)
        hourly_base = self.basic_salary / 30.0 / 8.0
        return hourly_base * actual_hours * self.ot_rate_multiplier()

    def approve(
        self,
        *,
        manager_id: ObjectId,
        approved_hours: float | None = None,
        comment: str | None = None,
    ) -> None:
        if self.status != OvertimeStatus.PENDING:
            raise ValueError("Only pending OT request can be approved")

        hours = self.requested_hours() if approved_hours is None else float(approved_hours)
        if hours < 0:
            raise ValueError("approved_hours cannot be negative")
        if hours > self.requested_hours():
            raise ValueError("approved_hours cannot exceed requested hours")

        self.status = OvertimeStatus.APPROVED
        self.manager_id = manager_id
        self.manager_comment = (comment or "").strip() or None
        self.approved_hours = hours
        self.calculated_payment = self.calculate_payment(hours)
        self.lifecycle.touch(now_utc())

    def reject(self, *, manager_id: ObjectId, comment: str | None = None) -> None:
        if self.status != OvertimeStatus.PENDING:
            raise ValueError("Only pending OT request can be rejected")

        self.status = OvertimeStatus.REJECTED
        self.manager_id = manager_id
        self.manager_comment = (comment or "").strip() or None
        self.lifecycle.touch(now_utc())

    def cancel(self, *, actor_id: ObjectId) -> None:
        if self.status != OvertimeStatus.PENDING:
            raise ValueError("Only pending OT request can be cancelled")

        self.status = OvertimeStatus.CANCELLED
        self.lifecycle.touch(now_utc())

    def is_payable(self) -> bool:
        return self.status == OvertimeStatus.APPROVED and self.approved_hours > 0

    def is_deleted(self) -> bool:
        return self.lifecycle.is_deleted()

    def soft_delete(self, *, actor_id: ObjectId | str) -> None:
        self.lifecycle.soft_delete(actor_id=str(actor_id))