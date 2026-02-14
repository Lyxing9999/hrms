# app/contexts/hrms/factories/public_holiday_factory.py
from bson import ObjectId
from datetime import date as date_type

from app.contexts.hrms.domain.public_holiday import PublicHoliday


class PublicHolidayFactory:
    def __init__(self, holiday_read_model):
        self._read = holiday_read_model

    def create_holiday(self, *, payload: dict, created_by: str | ObjectId | None) -> PublicHoliday:
        name = (payload.get("name") or "").strip()
        date_val = payload["date"]
        
        # Check if holiday already exists on this date
        existing = self._read.get_by_date(date_val)
        if existing:
            raise ValueError(f"A public holiday already exists on {date_val}")
        
        return PublicHoliday(
            name=name,
            name_kh=payload.get("name_kh"),
            date=date_val,
            is_paid=payload.get("is_paid", True),
            description=payload.get("description"),
            created_by=created_by,
        )
