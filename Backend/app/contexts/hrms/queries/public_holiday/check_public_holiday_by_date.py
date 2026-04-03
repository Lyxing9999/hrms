from __future__ import annotations


class CheckPublicHolidayByDateQuery:
    def __init__(self, *, public_holiday_repository) -> None:
        self.public_holiday_repository = public_holiday_repository

    def execute(self, *, date):
        return self.public_holiday_repository.find_by_date(date)