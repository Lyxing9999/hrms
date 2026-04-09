from calendar import monthrange
from datetime import date, datetime, timedelta


class PayrollCalendarService:
    def _as_date(self, value):
        if value is None:
            return None
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, date):
            return value
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value).date()
            except ValueError:
                return date.fromisoformat(value)
        return value

    def month_range(self, month: str) -> tuple[date, date]:
        year, month_num = map(int, month.split("-"))
        start = date(year, month_num, 1)
        end = date(year, month_num, monthrange(year, month_num)[1])
        return start, end

    def iter_dates(self, start: date, end: date):
        current = start
        while current <= end:
            yield current
            current += timedelta(days=1)

    def resolve_employee_active_range(
        self,
        *,
        month_start: date,
        month_end: date,
        employee: dict,
    ) -> tuple[date, date] | None:
        contract = employee.get("contract") or {}

        contract_start = self._as_date(contract.get("start_date"))
        contract_end = self._as_date(contract.get("end_date"))
        join_date = self._as_date(employee.get("join_date") or employee.get("start_date"))

        active_start = self._as_date(month_start)
        active_end = self._as_date(month_end)

        if contract_start:
            active_start = max(active_start, contract_start)
        elif join_date:
            active_start = max(active_start, join_date)

        if contract_end:
            active_end = min(active_end, contract_end)

        if active_end < active_start:
            return None

        return active_start, active_end

    def count_expected_working_days(
        self,
        *,
        month: str,
        employee: dict,
        working_schedule,
        public_holidays: list,
    ) -> dict:
        month_start, month_end = self.month_range(month)

        active_range = self.resolve_employee_active_range(
            month_start=month_start,
            month_end=month_end,
            employee=employee,
        )
        if not active_range:
            return {
                "expected_working_days": 0,
                "paid_holiday_days": 0,
                "working_dates": [],
                "holiday_dates": [],
            }

        active_start, active_end = active_range

        holiday_dates = set()
        for holiday in public_holidays:
            holiday_date = getattr(holiday, "date", None) or getattr(holiday, "holiday_date", None)
            holiday_date = self._as_date(holiday_date)
            if holiday_date:
                holiday_dates.add(holiday_date)

        expected_working_days = 0
        paid_holiday_days = 0
        working_dates: list[date] = []
        counted_holiday_dates: list[date] = []

        for current_date in self.iter_dates(active_start, active_end):
            weekday = current_date.weekday()

            if working_schedule.is_weekend(weekday):
                continue

            if current_date in holiday_dates:
                paid_holiday_days += 1
                counted_holiday_dates.append(current_date)
                continue

            expected_working_days += 1
            working_dates.append(current_date)

        return {
            "expected_working_days": expected_working_days,
            "paid_holiday_days": paid_holiday_days,
            "working_dates": working_dates,
            "holiday_dates": counted_holiday_dates,
        }