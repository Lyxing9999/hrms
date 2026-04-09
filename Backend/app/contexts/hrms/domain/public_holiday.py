from __future__ import annotations

from datetime import date as date_type
from bson import ObjectId

from app.contexts.hrms.errors.holiday_exceptions import HolidayNameRequiredException
from app.contexts.shared.lifecycle.domain import Lifecycle, now_utc


class PublicHoliday:
    def __init__(
        self,
        *,
        name: str,
        date: date_type,
        is_paid: bool = True,
        id: ObjectId | None = None,
        name_kh: str | None = None,
        description: str | None = None,
        created_by: ObjectId | None = None,
        lifecycle: Lifecycle | None = None,
    ) -> None:
        self.id = id or ObjectId()
        self.name = (name or "").strip()
        self.name_kh = (name_kh or "").strip() if name_kh else None
        self.date = date
        self.is_paid = bool(is_paid)
        self.description = (description or "").strip() if description else None
        self.created_by = created_by
        self.lifecycle = lifecycle or Lifecycle()

        if not self.name:
            raise HolidayNameRequiredException()

    def update_date(self, new_date: date_type) -> None:
        self.date = new_date
        self.lifecycle.touch(now_utc())

    def rename(self, name: str, name_kh: str | None = None) -> None:
        if not (name or "").strip():
            raise HolidayNameRequiredException()
        self.name = name.strip()
        self.name_kh = name_kh.strip() if name_kh else None
        self.lifecycle.touch(now_utc())

    def set_paid(self, is_paid: bool) -> None:
        self.is_paid = bool(is_paid)
        self.lifecycle.touch(now_utc())

    def is_deleted(self) -> bool:
        return self.lifecycle.is_deleted()

    def soft_delete(self, *, actor_id: ObjectId | str) -> None:
        self.lifecycle.soft_delete(actor_id=str(actor_id))