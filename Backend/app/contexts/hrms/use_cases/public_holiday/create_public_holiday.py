from __future__ import annotations

from datetime import timezone

from app.contexts.hrms.domain.public_holiday import PublicHoliday
from app.contexts.hrms.errors.holiday_exceptions import DuplicateHolidayDateException


class CreatePublicHolidayUseCase:
    def __init__(self, *, public_holiday_repository) -> None:
        self.public_holiday_repository = public_holiday_repository

    def execute(self, *, payload, created_by_user_id):
        existing = self.public_holiday_repository.find_by_date(payload.date)
        if existing and not existing.is_deleted():
            raise DuplicateHolidayDateException(str(payload.date))

        holiday = PublicHoliday(
            name=payload.name,
            name_kh=payload.name_kh,
            date=payload.date,
            is_paid=payload.is_paid,
            description=payload.description,
            created_by=created_by_user_id,
        )

        return self.public_holiday_repository.save(holiday)