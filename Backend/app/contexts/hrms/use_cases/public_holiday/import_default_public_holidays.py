from __future__ import annotations

from app.contexts.hrms.domain.public_holiday import PublicHoliday


class ImportDefaultPublicHolidaysUseCase:
    def __init__(
        self,
        *,
        public_holiday_repository,
        cambodia_public_holiday_provider,
    ) -> None:
        self.public_holiday_repository = public_holiday_repository
        self.cambodia_public_holiday_provider = cambodia_public_holiday_provider

    def execute(self, *, year: int, created_by_user_id):
        defaults = self.cambodia_public_holiday_provider.get_cambodia_holidays(year)

        imported = []
        skipped_dates: list[str] = []

        for item in defaults:
            existing = self.public_holiday_repository.find_by_date(item["date"])
            if existing:
                skipped_dates.append(item["date"].isoformat())
                continue

            holiday = PublicHoliday(
                name=item["name"],
                name_kh=item.get("name_kh"),
                date=item["date"],
                is_paid=item.get("is_paid", True),
                description=item.get("description"),
                created_by=created_by_user_id,
            )
            holiday = self.public_holiday_repository.save(holiday)
            imported.append(holiday)

        return {
            "year": year,
            "imported_count": len(imported),
            "skipped_count": len(skipped_dates),
            "imported": imported,
            "skipped_dates": skipped_dates,
        }