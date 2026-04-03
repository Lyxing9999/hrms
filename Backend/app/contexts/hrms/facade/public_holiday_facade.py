from __future__ import annotations


class PublicHolidayFacade:
    def __init__(
        self,
        *,
        create_public_holiday,
        update_public_holiday,
        soft_delete_public_holiday,
        restore_public_holiday,
        list_public_holidays,
        get_public_holiday,
        check_public_holiday_by_date,
        import_default_public_holidays,
    ) -> None:
        self._create_public_holiday = create_public_holiday
        self._update_public_holiday = update_public_holiday
        self._soft_delete_public_holiday = soft_delete_public_holiday
        self._restore_public_holiday = restore_public_holiday
        self._list_public_holidays = list_public_holidays
        self._get_public_holiday = get_public_holiday
        self._check_public_holiday_by_date = check_public_holiday_by_date
        self._import_default_public_holidays = import_default_public_holidays

    def create(self, **kwargs):
        return self._create_public_holiday.execute(**kwargs)

    def update(self, **kwargs):
        return self._update_public_holiday.execute(**kwargs)

    def soft_delete(self, **kwargs):
        return self._soft_delete_public_holiday.execute(**kwargs)

    def restore(self, **kwargs):
        return self._restore_public_holiday.execute(**kwargs)

    def list(self, **kwargs):
        return self._list_public_holidays.execute(**kwargs)

    def get(self, **kwargs):
        return self._get_public_holiday.execute(**kwargs)

    def check_by_date(self, **kwargs):
        return self._check_public_holiday_by_date.execute(**kwargs)

    def import_defaults(self, **kwargs):
        return self._import_default_public_holidays.execute(**kwargs)