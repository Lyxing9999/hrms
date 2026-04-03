from __future__ import annotations


class ListPublicHolidaysQuery:
    def __init__(self, *, public_holiday_repository) -> None:
        self.public_holiday_repository = public_holiday_repository

    def execute(
        self,
        *,
        year: int | None = None,
        include_deleted: bool = False,
        deleted_only: bool = False,
    ):
        return self.public_holiday_repository.list_holidays(
            year=year,
            include_deleted=include_deleted,
            deleted_only=deleted_only,
        )