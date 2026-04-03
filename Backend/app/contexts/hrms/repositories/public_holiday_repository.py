from __future__ import annotations

from datetime import date as date_type
from bson import ObjectId
from pymongo.database import Database

from app.contexts.hrms.domain.public_holiday import PublicHoliday
from app.contexts.hrms.mapper.public_holiday_mapper import PublicHolidayMapper
from app.contexts.shared.model_converter import mongo_converter


class MongoPublicHolidayRepository:
    def __init__(self, db: Database):
        self.collection = db["public_holidays"]
        self.mapper = PublicHolidayMapper()

    @staticmethod
    def _oid(v) -> ObjectId | None:
        return mongo_converter.convert_to_object_id(v)

    @staticmethod
    def _date_str(v) -> str | None:
        if v is None:
            return None
        if isinstance(v, date_type):
            return v.isoformat()
        return str(v)

    def save(self, holiday: PublicHoliday) -> PublicHoliday:
        doc = self.mapper.to_persistence(holiday)
        self.collection.replace_one({"_id": doc["_id"]}, doc, upsert=True)
        return holiday

    def find_by_id(self, holiday_id) -> PublicHoliday | None:
        holiday_id = self._oid(holiday_id)
        doc = self.collection.find_one({
            "_id": holiday_id,
            "lifecycle.deleted_at": None,
        })
        return self.mapper.to_domain(doc) if doc else None

    def find_by_id_including_deleted(self, holiday_id) -> PublicHoliday | None:
        holiday_id = self._oid(holiday_id)
        doc = self.collection.find_one({"_id": holiday_id})
        return self.mapper.to_domain(doc) if doc else None

    def find_by_date(self, holiday_date: date_type) -> PublicHoliday | None:
        doc = self.collection.find_one({
            "date": self._date_str(holiday_date),
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
            start_date = date_type(year, 1, 1).isoformat()
            end_date = date_type(year, 12, 31).isoformat()
            query["date"] = {"$gte": start_date, "$lte": end_date}

        if deleted_only:
            query["lifecycle.deleted_at"] = {"$ne": None}
        elif not include_deleted:
            query["lifecycle.deleted_at"] = None

        docs = self.collection.find(query).sort("date", 1)
        return [self.mapper.to_domain(doc) for doc in docs]

    def delete(self, holiday_id: ObjectId) -> None:
        self.collection.delete_one({"_id": holiday_id})