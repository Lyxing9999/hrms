# app/contexts/hrms/repositories/leave_repository.py
from typing import Optional
from bson import ObjectId
from pymongo.collection import Collection

from app.contexts.shared.lifecycle.filters import not_deleted, by_show_deleted
from app.contexts.shared.lifecycle.domain import now_utc as lifecycle_now_utc
from app.contexts.hrms.domain.leave import LeaveRequest
from app.contexts.hrms.mapper.leave_mapper import LeaveMapper

class MongoLeaveRepository:
    def __init__(self, collection: Collection):
        self.collection = collection
        self.mapper = LeaveMapper()

    def find_one(self, id: ObjectId, *, include_deleted: bool = False) -> Optional[LeaveRequest]:
        show = "all" if include_deleted else "active"
        raw = self.collection.find_one(by_show_deleted(show, {"_id": id}))
        return None if not raw else self.mapper.to_domain(raw)

    def save(self, payload: dict) -> LeaveRequest:
        res = self.collection.insert_one(dict(payload))
        leave = self.find_one(res.inserted_id)
        if leave is None:
            raise RuntimeError(f"Leave insert ok but load failed: {res.inserted_id}")
        return leave

    def update(self, leave_id: ObjectId, payload: dict) -> Optional[LeaveRequest]:
        data = dict(payload)
        data.pop("_id", None)
        
        # Extract lifecycle separately to handle it properly
        lifecycle_data = data.pop("lifecycle", None)
        
        update_doc = {"$set": {**data, "lifecycle.updated_at": lifecycle_now_utc()}}
        
        # If lifecycle has deleted_at or deleted_by, update those fields
        if lifecycle_data:
            if "deleted_at" in lifecycle_data:
                update_doc["$set"]["lifecycle.deleted_at"] = lifecycle_data["deleted_at"]
            if "deleted_by" in lifecycle_data:
                update_doc["$set"]["lifecycle.deleted_by"] = lifecycle_data["deleted_by"]

        res = self.collection.update_one(
            {"_id": leave_id},  # Don't filter by deleted_at for updates
            update_doc,
        )
        if res.matched_count == 0:
            return None
        return self.find_one(leave_id, include_deleted=True)
