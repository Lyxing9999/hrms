from __future__ import annotations

from datetime import datetime, timezone
from zoneinfo import ZoneInfo

CAMBODIA_TZ = ZoneInfo("Asia/Phnom_Penh")


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def cambodia_now() -> datetime:
    return datetime.now(CAMBODIA_TZ)


def ensure_utc(dt: datetime | None) -> datetime | None:
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=CAMBODIA_TZ)
    return dt.astimezone(timezone.utc)


def to_cambodia(dt: datetime | None) -> datetime | None:
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=CAMBODIA_TZ)
    return dt.astimezone(CAMBODIA_TZ)


def cambodia_start_of_day_as_utc(dt: datetime) -> datetime:
    dt_kh = to_cambodia(dt)
    return dt_kh.replace(hour=0, minute=0, second=0, microsecond=0).astimezone(timezone.utc)