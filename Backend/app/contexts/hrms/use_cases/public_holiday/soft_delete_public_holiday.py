from __future__ import annotations

from app.contexts.hrms.errors.holiday_exceptions import PublicHolidayNotFoundException


class SoftDeletePublicHolidayUseCase:
    def __init__(self, *, public_holiday_repository) -> None:
        self.public_holiday_repository = public_holiday_repository

    def execute(self, *, holiday_id, actor_id):
        holiday = self.public_holiday_repository.find_by_id(holiday_id)
        if not holiday:
            raise PublicHolidayNotFoundException(str(holiday_id))

        holiday.soft_delete(actor_id=actor_id)
        return self.public_holiday_repository.save(holiday)