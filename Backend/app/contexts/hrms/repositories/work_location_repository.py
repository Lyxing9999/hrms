# app/contexts/hrms/repositories/work_location_repository.py
from typing import Optional
from bson import ObjectId
from pymongo.collection import Collection

from app.contexts.shared.lifecycle.filters import not_deleted, by_show_deleted
from app.contexts.shared.lifecycle.domain import now_utc as lifecycle_now_utc
from app.contexts.hrms.mapper.work_location_mapper import WorkLocationMapper
from app.contexts.hrms.domain.work_location import WorkLocation


class MongoWorkLocationRepository:
    def __init__(self, collection: Collection):
        self.collection = collection
        self.mapper = WorkLocationMapper()

    def find_one(self, id: ObjectId, *, include_deleted: bool = False) -> Optional[WorkLocation]:
        show = "all" if include_deleted else "active"
        raw = self.collection.find_one(by_show_deleted(show, {"_id": id}))
        return None if not raw else self.mapper.to_domain(raw)

    def save(self, payload: dict) -> WorkLocation:
        res = self.collection.insert_one(dict(payload))
        location = self.find_one(res.inserted_id)
        if location is None:
            raise RuntimeError(f"WorkLocation insert ok but load failed: {res.inserted_id}")
        return location

    def update(self, location_id: ObjectId, payload: dict) -> Optional[WorkLocation]:
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
            {"_id": location_id},
            update_doc,
        )
        if res.matched_count == 0:
            return None
        return self.find_one(location_id, include_deleted=True)
