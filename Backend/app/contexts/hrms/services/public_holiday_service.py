# app/contexts/hrms/services/public_holiday_service.py
from __future__ import annotations
from bson import ObjectId
from datetime import date as date_type
from pymongo.database import Database

from app.contexts.hrms.read_models.public_holiday_read_model import PublicHolidayReadModel
from app.contexts.hrms.repositories.public_holiday_repository import MongoPublicHolidayRepository
from app.contexts.hrms.factories.public_holiday_factory import PublicHolidayFactory
from app.contexts.hrms.mapper.public_holiday_mapper import PublicHolidayMapper
from app.contexts.hrms.domain.public_holiday import PublicHoliday
from app.contexts.shared.lifecycle.filters import ShowDeleted
from app.contexts.shared.lifecycle.domain import now_utc
from app.contexts.shared.model_converter import mongo_converter


class PublicHolidayNotFoundException(Exception):
    def __init__(self, holiday_id: str):
        super().__init__(f"Public holiday not found: {holiday_id}")


class PublicHolidayService:
    def __init__(self, db: Database):
        self.db = db
        self._read = PublicHolidayReadModel(db)
        self._repo = MongoPublicHolidayRepository(db["public_holidays"])
        self._mapper = PublicHolidayMapper()
        self._factory = PublicHolidayFactory(self._read)

    def _oid(self, v: str | ObjectId | None) -> ObjectId | None:
        return mongo_converter.convert_to_object_id(v)

    # -------------------------
    # LIST
    # -------------------------
    def list_holidays(
        self,
        *,
        q: str = "",
        page: int = 1,
        page_size: int = 10,
        year: int | None = None,
        show_deleted: ShowDeleted = "active",
    ) -> tuple[list[PublicHoliday], int]:
        items, total = self._read.get_page(
            page=page,
            page_size=page_size,
            q=q,
            year=year,
            show_deleted=show_deleted,
        )
        domains = [self._mapper.to_domain(x) for x in items]
        return domains, int(total)

    # -------------------------
    # GET ONE
    # -------------------------
    def get_holiday(self, holiday_id: str | ObjectId, *, show_deleted: ShowDeleted = "active") -> PublicHoliday:
        raw = self._read.get_by_id(self._oid(holiday_id), show_deleted=show_deleted)
        if not raw:
            raise PublicHolidayNotFoundException(str(holiday_id))
        return self._mapper.to_domain(raw)

    # -------------------------
    # CHECK IF DATE IS HOLIDAY
    # -------------------------
    def is_holiday(self, date: date_type) -> bool:
        """Check if a specific date is a public holiday"""
        raw = self._read.get_by_date(date, show_deleted="active")
        return raw is not None

    # -------------------------
    # GET HOLIDAYS IN RANGE
    # -------------------------
    def get_holidays_in_range(self, start_date: date_type, end_date: date_type) -> list[PublicHoliday]:
        """Get all holidays within a date range"""
        items = self._read.get_holidays_in_range(start_date, end_date, show_deleted="active")
        return [self._mapper.to_domain(x) for x in items]

    # -------------------------
    # GET HOLIDAYS BY YEAR
    # -------------------------
    def get_holidays_by_year(self, year: int) -> list[PublicHoliday]:
        """Get all holidays for a specific year"""
        items = self._read.get_holidays_by_year(year, show_deleted="active")
        return [self._mapper.to_domain(x) for x in items]

    # -------------------------
    # CREATE
    # -------------------------
    def create_holiday(self, payload, *, created_by_user_id: str | ObjectId) -> PublicHoliday:
        actor_oid = self._oid(created_by_user_id)
        
        p = payload.model_dump()
        
        holiday = self._factory.create_holiday(payload=p, created_by=actor_oid)
        saved = self._repo.save(self._mapper.to_persistence(holiday))
        
        return saved

    # -------------------------
    # UPDATE
    # -------------------------
    def update_holiday(self, holiday_id: str | ObjectId, payload, *, actor_id: str | ObjectId) -> PublicHoliday:
        holiday = self.get_holiday(holiday_id, show_deleted="active")
        
        p = payload.model_dump(exclude_unset=True)
        
        # Update fields
        if "name" in p and p["name"]:
            holiday.name = str(p["name"]).strip()
        
        if "name_kh" in p:
            holiday.name_kh = str(p["name_kh"]).strip() if p["name_kh"] else None
        
        if "date" in p and p["date"]:
            # Check if new date conflicts with existing holiday
            existing = self._read.get_by_date(p["date"])
            if existing and str(existing["_id"]) != str(holiday.id):
                raise ValueError(f"A public holiday already exists on {p['date']}")
            holiday.update_date(p["date"])
        
        if "is_paid" in p:
            holiday.set_paid(p["is_paid"])
        
        if "description" in p:
            holiday.description = str(p["description"]).strip() if p["description"] else None
        
        holiday.lifecycle.touch(now_utc())
        
        updated = self._repo.update(self._oid(holiday.id), self._mapper.to_persistence(holiday))
        if not updated:
            raise PublicHolidayNotFoundException(str(holiday_id))
        
        return updated

    # -------------------------
    # SOFT DELETE
    # -------------------------
    def soft_delete_holiday(self, holiday_id: str | ObjectId, *, actor_id: str | ObjectId) -> PublicHoliday:
        holiday = self.get_holiday(holiday_id, show_deleted="active")
        
        holiday.soft_delete(actor_id=actor_id)
        
        updated = self._repo.update(self._oid(holiday.id), self._mapper.to_persistence(holiday))
        if not updated:
            raise PublicHolidayNotFoundException(str(holiday_id))
        
        return updated

    # -------------------------
    # RESTORE
    # -------------------------
    def restore_holiday(self, holiday_id: str | ObjectId) -> PublicHoliday:
        holiday = self.get_holiday(holiday_id, show_deleted="deleted_only")
        
        holiday.lifecycle.restore()
        
        updated = self._repo.update(self._oid(holiday.id), self._mapper.to_persistence(holiday))
        if not updated:
            raise PublicHolidayNotFoundException(str(holiday_id))
        
        return updated
