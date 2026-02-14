# app/contexts/hrms/repositories/public_holiday_repository.py
from typing import Optional
from bson import ObjectId
from pymongo.collection import Collection

from app.contexts.shared.lifecycle.filters import not_deleted, by_show_deleted
from app.contexts.shared.lifecycle.domain import now_utc as lifecycle_now_utc
from app.contexts.hrms.mapper.public_holiday_mapper import PublicHolidayMapper
from app.contexts.hrms.domain.public_holiday import PublicHoliday


class MongoPublicHolidayRepository:
    def __init__(self, collection: Collection):
        self.collection = collection
        self.mapper = PublicHolidayMapper()

    def find_one(self, id: ObjectId, *, include_deleted: bool = False) -> Optional[PublicHoliday]:
        show = "all" if include_deleted else "active"
        raw = self.collection.find_one(by_show_deleted(show, {"_id": id}))
        return None if not raw else self.mapper.to_domain(raw)

    def save(self, payload: dict) -> PublicHoliday:
        res = self.collection.insert_one(dict(payload))
        holiday = self.find_one(res.inserted_id)
        if holiday is None:
            raise RuntimeError(f"PublicHoliday insert ok but load failed: {res.inserted_id}")
        return holiday

    def update(self, holiday_id: ObjectId, payload: dict) -> Optional[PublicHoliday]:
        data = dict(payload)
        data.pop("_id", None)
        
        lifecycle_data = data.pop("lifecycle", None)
        
        update_doc = {"$set": {**data, "lifecycle.updated_at": lifecycle_now_utc()}}
        
        if lifecycle_data:
            if "deleted_at" in lifecycle_data:
                update_doc["$set"]["lifecycle.deleted_at"] = lifecycle_data["deleted_at"]
            if "deleted_by" in lifecycle_data:
                update_doc["$set"]["lifecycle.deleted_by"] = lifecycle_data["deleted_by"]

        res = self.collection.update_one(
            {"_id": holiday_id},
            update_doc,
        )
        if res.matched_count == 0:
            return None
        return self.find_one(holiday_id, include_deleted=True)
