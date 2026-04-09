from __future__ import annotations

from app.contexts.hrms.errors.holiday_exceptions import (
    DuplicateHolidayDateException,
    PublicHolidayNotFoundException,
)


class UpdatePublicHolidayUseCase:
    def __init__(self, *, public_holiday_repository) -> None:
        self.public_holiday_repository = public_holiday_repository

    def execute(self, *, holiday_id, payload, actor_id):
        holiday = self.public_holiday_repository.find_by_id(holiday_id)
        if not holiday:
            raise PublicHolidayNotFoundException(str(holiday_id))

        if payload.name is not None or payload.name_kh is not None:
            holiday.rename(
                name=payload.name if payload.name is not None else holiday.name,
                name_kh=payload.name_kh if payload.name_kh is not None else holiday.name_kh,
            )

        if payload.date is not None and payload.date != holiday.date:
            existing = self.public_holiday_repository.find_by_date(payload.date)
            if existing and str(existing.id) != str(holiday.id) and not existing.is_deleted():
                raise DuplicateHolidayDateException(str(payload.date))
            holiday.update_date(payload.date)

        if payload.is_paid is not None:
            holiday.set_paid(payload.is_paid)

        if payload.description is not None:
            holiday.description = (payload.description or "").strip() or None
            holiday.lifecycle.touch()

        return self.public_holiday_repository.save(holiday)