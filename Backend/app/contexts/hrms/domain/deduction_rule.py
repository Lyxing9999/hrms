from __future__ import annotations

from enum import Enum
from bson import ObjectId

from app.contexts.shared.lifecycle.domain import Lifecycle, now_utc


class DeductionType(str, Enum):
    LATE = "late"
    EARLY_LEAVE = "early_leave"
    ABSENT = "absent"


class DeductionRule:
    """
    Example:
    - 1 to 60 late minutes => 5%
    - 61 to 120 late minutes => 10%
    - 121 to 180 late minutes => 15%
    - 181+ late minutes => 20%
    """

    def __init__(
        self,
        *,
        type: DeductionType | str,
        min_minutes: int,
        max_minutes: int | None,
        deduction_percentage: float,
        id: ObjectId | None = None,
        is_active: bool = True,
        created_by: ObjectId | None = None,
        lifecycle: Lifecycle | None = None,
    ) -> None:
        self.id = id or ObjectId()
        self.type = DeductionType(str(type).strip().lower())
        self.min_minutes = int(min_minutes)
        self.max_minutes = int(max_minutes) if max_minutes is not None else None
        self.deduction_percentage = float(deduction_percentage)
        self.is_active = bool(is_active)
        self.created_by = created_by
        self.lifecycle = lifecycle or Lifecycle()

        if self.min_minutes < 0:
            raise ValueError("min_minutes cannot be negative")
        if self.max_minutes is not None and self.max_minutes < self.min_minutes:
            raise ValueError("max_minutes cannot be less than min_minutes")
        if not (0 <= self.deduction_percentage <= 100):
            raise ValueError("deduction_percentage must be between 0 and 100")

    def applies_to(self, minutes: int) -> bool:
        if minutes < self.min_minutes:
            return False
        if self.max_minutes is None:
            return True
        return minutes <= self.max_minutes

    def calculate_deduction(self, daily_salary: float) -> float:
        return float(daily_salary) * (self.deduction_percentage / 100.0)

    def activate(self) -> None:
        self.is_active = True
        self.lifecycle.touch(now_utc())

    def deactivate(self) -> None:
        self.is_active = False
        self.lifecycle.touch(now_utc())

    def update_percentage(self, new_percentage: float) -> None:
        if not (0 <= new_percentage <= 100):
            raise ValueError("deduction_percentage must be between 0 and 100")
        self.deduction_percentage = float(new_percentage)
        self.lifecycle.touch(now_utc())

    def is_deleted(self) -> bool:
        return self.lifecycle.is_deleted()

    def soft_delete(self, *, actor_id: ObjectId | str) -> None:
        self.lifecycle.soft_delete(actor_id=str(actor_id))