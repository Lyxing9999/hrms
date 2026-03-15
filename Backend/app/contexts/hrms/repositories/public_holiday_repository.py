from __future__ import annotations

from datetime import date as date_type
from bson import ObjectId
from pymongo.database import Database

from app.contexts.hrms.domain.public_holiday import PublicHoliday
from app.contexts.hrms.mapper.public_holiday_mapper import PublicHolidayMapper
from app.contexts.hrms.errors.public_holiday_exceptions import PublicHolidayNotFoundException


class MongoPublicHolidayRepository:
    def __init__(self, db: Database):
        self.collection = db["hr_public_holidays"]
        self.mapper = PublicHolidayMapper()

    def save(self, holiday: PublicHoliday) -> PublicHoliday:
        doc = self.mapper.to_persistence(holiday)
        self.collection.replace_one({"_id": doc["_id"]}, doc, upsert=True)
        return holiday

    def find_by_id(self, holiday_id: ObjectId) -> PublicHoliday:
        doc = self.collection.find_one({"_id": holiday_id})
        if not doc:
            raise PublicHolidayNotFoundException(holiday_id)
        return self.mapper.to_domain(doc)

    def find_by_date(self, holiday_date: date_type) -> PublicHoliday | None:
        doc = self.collection.find_one({
            "date": holiday_date,
            "lifecycle.deleted_at": None,
        })
        return self.mapper.to_domain(doc) if doc else None

    def list_holidays(
        self,
        *,
        year: int | None = None,
        include_deleted: bool = False,
        deleted_only: bool = False,
    ) -> list[PublicHoliday]:
        query = {}

        if year is not None:
            query["year"] = year  # TODO: or use date-range query if year is not stored

        if deleted_only:
            query["lifecycle.deleted_at"] = {"$ne": None}
        elif not include_deleted:
            query["lifecycle.deleted_at"] = None

        docs = self.collection.find(query).sort("date", 1)
        return [self.mapper.to_domain(doc) for doc in docs]

    def delete(self, holiday_id: ObjectId) -> None:
        self.collection.delete_one({"_id": holiday_id})