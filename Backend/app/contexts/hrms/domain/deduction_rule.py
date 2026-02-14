# app/contexts/hrms/domain/deduction_rule.py
from __future__ import annotations
from enum import Enum
from bson import ObjectId

from app.contexts.shared.lifecycle.domain import Lifecycle, now_utc
from app.contexts.hrms.errors.deduction_exceptions import (
    InvalidDeductionRangeException,
    InvalidDeductionPercentageException,
)


class DeductionType(str, Enum):
    LATE = "late"
    ABSENT = "absent"
    EARLY_LEAVE = "early_leave"


class DeductionRule:
    """
    Defines deduction rules for late arrivals, absences, and early leaves.
    Example: 1-30 minutes late = 5% deduction
    """
    
    def __init__(
        self,
        *,
        type: DeductionType | str,
        min_minutes: int,
        max_minutes: int,
        deduction_percentage: float,
        id: ObjectId | None = None,
        is_active: bool = True,
        created_by: ObjectId | None = None,
        lifecycle: Lifecycle | None = None,
    ) -> None:
        self.id = id or ObjectId()
        self.type = DeductionType(str(type).strip().lower())
        
        # Validate minute range
        if min_minutes < 0 or max_minutes < min_minutes:
            raise InvalidDeductionRangeException(min_minutes, max_minutes)
        
        self.min_minutes = int(min_minutes)
        self.max_minutes = int(max_minutes)
        
        # Validate percentage (0-100%)
        if not (0 <= deduction_percentage <= 100):
            raise InvalidDeductionPercentageException(deduction_percentage)
        
        self.deduction_percentage = float(deduction_percentage)
        self.is_active = bool(is_active)
        self.created_by = created_by
        self.lifecycle = lifecycle or Lifecycle()
    
    def applies_to(self, minutes: int) -> bool:
        """Check if this rule applies to given minutes"""
        return self.min_minutes <= minutes <= self.max_minutes
    
    def calculate_deduction(self, daily_salary: float) -> float:
        """Calculate deduction amount"""
        return daily_salary * (self.deduction_percentage / 100.0)
    
    def activate(self) -> None:
        """Activate this rule"""
        self.is_active = True
        self.lifecycle.touch(now_utc())
    
    def deactivate(self) -> None:
        """Deactivate this rule"""
        self.is_active = False
        self.lifecycle.touch(now_utc())
    
    def update_percentage(self, new_percentage: float) -> None:
        """Update deduction percentage"""
        if not (0 <= new_percentage <= 100):
            raise InvalidDeductionPercentageException(new_percentage)
        
        self.deduction_percentage = float(new_percentage)
        self.lifecycle.touch(now_utc())
    
    def is_deleted(self) -> bool:
        return self.lifecycle.is_deleted()
    
    def soft_delete(self, *, actor_id: str | ObjectId) -> None:
        """Soft delete the rule"""
        self.lifecycle.soft_delete(actor_id=str(actor_id))
