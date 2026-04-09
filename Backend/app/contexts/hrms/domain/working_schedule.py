from __future__ import annotations

from datetime import time as time_type
from bson import ObjectId

from app.contexts.hrms.errors.schedule_exceptions import (
    InvalidWorkingDaysException,
    InvalidWorkingHoursException,
    ScheduleNameRequiredException,
    WorkingDaysRequiredException,
)
from app.contexts.shared.lifecycle.domain import Lifecycle, now_utc


class WorkingSchedule:
    """
    Default business rule:
    - Monday-Friday are working days => [0,1,2,3,4]
    - Saturday/Sunday are weekends => [5,6]
    """

    def __init__(
        self,
        *,
        name: str,
        start_time: time_type,
        end_time: time_type,
        working_days: list[int],
        id: ObjectId | None = None,
        weekend_days: list[int] | None = None,
        total_hours_per_day: float | None = None,
        is_default: bool = False,
        created_by: ObjectId | None = None,
        lifecycle: Lifecycle | None = None,
    ) -> None:
        self.id = id or ObjectId()
        self.name = (name or "").strip()
        self.start_time = start_time
        self.end_time = end_time
        self.working_days = sorted(set(working_days))
        self.weekend_days = (
            sorted(set(weekend_days))
            if weekend_days is not None
            else sorted(set(range(7)) - set(self.working_days))
        )
        self.total_hours_per_day = (
            float(total_hours_per_day)
            if total_hours_per_day is not None
            else self._calculate_daily_hours(start_time, end_time)
        )
        self.is_default = bool(is_default)
        self.created_by = created_by
        self.lifecycle = lifecycle or Lifecycle()

        if not self.name:
            raise ScheduleNameRequiredException()
        if end_time <= start_time:
            raise InvalidWorkingHoursException(start_time, end_time)
        if not self.working_days:
            raise WorkingDaysRequiredException()
        if not all(0 <= d <= 6 for d in self.working_days):
            raise InvalidWorkingDaysException(self.working_days)

    def _calculate_daily_hours(self, start_time: time_type, end_time: time_type) -> float:
        hours = end_time.hour - start_time.hour
        minutes = end_time.minute - start_time.minute
        return hours + (minutes / 60.0)

    def is_working_day(self, weekday: int) -> bool:
        return weekday in self.working_days

    def is_weekend(self, weekday: int) -> bool:
        return weekday in self.weekend_days

    def update_times(self, start_time: time_type, end_time: time_type) -> None:
        if end_time <= start_time:
            raise InvalidWorkingHoursException(start_time, end_time)
        self.start_time = start_time
        self.end_time = end_time
        self.total_hours_per_day = self._calculate_daily_hours(start_time, end_time)
        self.lifecycle.touch(now_utc())

    def update_working_days(self, working_days: list[int]) -> None:
        if not working_days:
            raise WorkingDaysRequiredException()
        if not all(0 <= d <= 6 for d in working_days):
            raise InvalidWorkingDaysException(working_days)

        self.working_days = sorted(set(working_days))
        self.weekend_days = sorted(set(range(7)) - set(self.working_days))
        self.lifecycle.touch(now_utc())

    def set_as_default(self) -> None:
        self.is_default = True
        self.lifecycle.touch(now_utc())

    def is_deleted(self) -> bool:
        return self.lifecycle.is_deleted()

    def soft_delete(self, *, actor_id: ObjectId | str) -> None:
        self.lifecycle.soft_delete(actor_id=str(actor_id))