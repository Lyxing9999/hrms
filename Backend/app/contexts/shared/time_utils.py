from __future__ import annotations

from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo

CAMBODIA_TZ = ZoneInfo("Asia/Phnom_Penh")


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def cambodia_now() -> datetime:
    return datetime.now(CAMBODIA_TZ)


def _coerce_datetime(value: datetime | date | str | None) -> datetime | None:
    if value is None:
        return None

    if isinstance(value, datetime):
        return value

    if isinstance(value, date):
        return datetime.combine(value, datetime.min.time())

    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        if text.endswith("Z"):
            text = f"{text[:-1]}+00:00"
        return datetime.fromisoformat(text)

    raise TypeError(f"Expected datetime/date/ISO string, got {type(value)}")


def ensure_utc(dt: datetime | date | str | None) -> datetime | None:
    dt = _coerce_datetime(dt)
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=CAMBODIA_TZ)
    return dt.astimezone(timezone.utc)


def to_cambodia(dt: datetime | date | str | None) -> datetime | None:
    dt = _coerce_datetime(dt)
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=CAMBODIA_TZ)
    return dt.astimezone(CAMBODIA_TZ)


def cambodia_start_of_day_as_utc(dt: datetime) -> datetime:
    dt_kh = to_cambodia(dt)
    return dt_kh.replace(hour=0, minute=0, second=0, microsecond=0).astimezone(timezone.utc)