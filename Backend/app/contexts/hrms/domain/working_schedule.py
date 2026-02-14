# app/contexts/hrms/domain/working_schedule.py
from __future__ import annotations
from datetime import time as time_type
from bson import ObjectId

from app.contexts.shared.lifecycle.domain import Lifecycle, now_utc
from app.contexts.hrms.errors.schedule_exceptions import (
    InvalidWorkingHoursException,
    InvalidWorkingDaysException,
)


class WorkingSchedule:
    """
    Defines working hours and days for employees.
    Default: Monday-Friday, 8:00-17:00 (8 hours/day)
    """
    
    def __init__(
        self,
        *,
        name: str,
        start_time: time_type,
        end_time: time_type,
        working_days: list[int],  # 0=Monday, 6=Sunday
        id: ObjectId | None = None,
        weekend_days: list[int] | None = None,
        total_hours_per_day: float | None = None,
        is_default: bool = False,
        created_by: ObjectId | None = None,
        lifecycle: Lifecycle | None = None,
    ) -> None:
        self.id = id or ObjectId()
        self.name = (name or "").strip()
        
        if not self.name:
            raise ValueError("Schedule name is required")
        
        self.start_time = start_time
        self.end_time = end_time
        
        # Validate time range
        if self.end_time <= self.start_time:
            raise InvalidWorkingHoursException(self.start_time, self.end_time)
        
        # Validate working days (0-6)
        if not working_days or not all(0 <= day <= 6 for day in working_days):
            raise InvalidWorkingDaysException(working_days)
        
        self.working_days = sorted(set(working_days))
        
        # Auto-calculate weekend days if not provided
        all_days = set(range(7))
        working_set = set(self.working_days)
        self.weekend_days = sorted(all_days - working_set) if weekend_days is None else sorted(set(weekend_days))
        
        # Calculate total hours per day
        if total_hours_per_day is None:
            hours = (self.end_time.hour - self.start_time.hour)
            minutes = (self.end_time.minute - self.start_time.minute)
            self.total_hours_per_day = hours + (minutes / 60.0)
        else:
            self.total_hours_per_day = float(total_hours_per_day)
        
        self.is_default = bool(is_default)
        self.created_by = created_by
        self.lifecycle = lifecycle or Lifecycle()
    
    def is_working_day(self, day_of_week: int) -> bool:
        """Check if given day (0=Monday, 6=Sunday) is a working day"""
        return day_of_week in self.working_days
    
    def is_weekend(self, day_of_week: int) -> bool:
        """Check if given day is a weekend"""
        return day_of_week in self.weekend_days
    
    def update_times(self, start_time: time_type, end_time: time_type) -> None:
        """Update working hours"""
        if end_time <= start_time:
            raise InvalidWorkingHoursException(start_time, end_time)
        
        self.start_time = start_time
        self.end_time = end_time
        
        # Recalculate hours
        hours = (self.end_time.hour - self.start_time.hour)
        minutes = (self.end_time.minute - self.start_time.minute)
        self.total_hours_per_day = hours + (minutes / 60.0)
        
        self.lifecycle.touch(now_utc())
    
    def update_working_days(self, working_days: list[int]) -> None:
        """Update working days"""
        if not working_days or not all(0 <= day <= 6 for day in working_days):
            raise InvalidWorkingDaysException(working_days)
        
        self.working_days = sorted(set(working_days))
        
        # Recalculate weekend days
        all_days = set(range(7))
        working_set = set(self.working_days)
        self.weekend_days = sorted(all_days - working_set)
        
        self.lifecycle.touch(now_utc())
    
    def set_as_default(self) -> None:
        """Mark this schedule as default"""
        self.is_default = True
        self.lifecycle.touch(now_utc())
    
    def is_deleted(self) -> bool:
        return self.lifecycle.is_deleted()
    
    def soft_delete(self, *, actor_id: str | ObjectId) -> None:
        """Soft delete the schedule"""
        self.lifecycle.soft_delete(actor_id=str(actor_id))
