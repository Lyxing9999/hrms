from __future__ import annotations


class GetPublicHolidayQuery:
    def __init__(self, *, public_holiday_repository) -> None:
        self.public_holiday_repository = public_holiday_repository

    def execute(self, *, holiday_id):
        holiday = self.public_holiday_repository.find_by_id(holiday_id)
        if not holiday:
            raise ValueError("Public holiday not found")
        return holiday