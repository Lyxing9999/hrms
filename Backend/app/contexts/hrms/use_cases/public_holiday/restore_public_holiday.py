from __future__ import annotations


class RestorePublicHolidayUseCase:
    def __init__(self, *, public_holiday_repository) -> None:
        self.public_holiday_repository = public_holiday_repository

    def execute(self, *, holiday_id):
        holiday = self.public_holiday_repository.find_by_id_including_deleted(holiday_id)
        if not holiday:
            raise ValueError("Public holiday not found")

        holiday.lifecycle.deleted_at = None
        holiday.lifecycle.deleted_by = None
        holiday.lifecycle.touch()

        return self.public_holiday_repository.save(holiday)