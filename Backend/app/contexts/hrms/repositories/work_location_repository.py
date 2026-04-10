# app/contexts/hrms/repositories/work_location_repository.py
from __future__ import annotations

from bson import ObjectId
from pymongo.database import Database

from app.contexts.hrms.mapper.work_location_mapper import WorkLocationMapper
from app.contexts.hrms.errors.location_exceptions import WorkLocationNotFoundException


class MongoWorkLocationRepository:
    def __init__(self, db: Database):
        self.collection = db["hr_work_locations"]
        self.mapper = WorkLocationMapper()

    def create(self, location):
        doc = self.mapper.to_persistence(location)
        result = self.collection.insert_one(doc)
        return self.find_by_id(result.inserted_id)

    def save(self, location):
        doc = self.mapper.to_persistence(location)
        self.collection.replace_one({"_id": doc["_id"]}, doc, upsert=True)
        return self.find_by_id_including_deleted(doc["_id"])

    def find_by_id(self, location_id):
        location_id = ObjectId(location_id) if not isinstance(location_id, ObjectId) else location_id
        doc = self.collection.find_one({
            "_id": location_id,
            "lifecycle.deleted_at": None,
        })
        if not doc:
            raise WorkLocationNotFoundException(str(location_id))
        return WorkLocationMapper.to_domain(doc)

    def find_by_id_including_deleted(self, location_id):
        location_id = ObjectId(location_id) if not isinstance(location_id, ObjectId) else location_id
        doc = self.collection.find_one({"_id": location_id})
        if not doc:
            raise WorkLocationNotFoundException(str(location_id))
        return self.mapper.to_domain(doc)

    def list_locations(
        self,
        *,
        q: str = "",
        status: str = "all",
        include_deleted: bool | None = None,
        deleted_only: bool | None = None,
        is_active: bool | None = None,
    ) -> list:
        query: dict = {}

        if q:
            query["$or"] = [
                {"name": {"$regex": q, "$options": "i"}},
                {"address": {"$regex": q, "$options": "i"}},
            ]

        # Backward-compatible branch: when explicit filter flags are not passed,
        # keep original semantics of the `status` query parameter.
        if include_deleted is None and deleted_only is None and is_active is None:
            if status == "active":
                query["lifecycle.deleted_at"] = None
                query["is_active"] = True
            elif status == "inactive":
                query["lifecycle.deleted_at"] = None
                query["is_active"] = False
            elif status == "deleted":
                query["lifecycle.deleted_at"] = {"$ne": None}
            else:
                # all (normal mode): include active + inactive, exclude deleted
                query["lifecycle.deleted_at"] = None
        else:
            # New explicit filter mode used by frontend:
            # - deleted_only=true => deleted records only
            # - include_deleted=true => include both deleted + non-deleted
            # - default => non-deleted only
            if deleted_only is None:
                deleted_only = status == "deleted"
            if include_deleted is None:
                include_deleted = status == "all"
            if is_active is None:
                if status == "active":
                    is_active = True
                elif status == "inactive":
                    is_active = False

            if deleted_only:
                query["lifecycle.deleted_at"] = {"$ne": None}
            elif include_deleted:
                pass
            else:
                query["lifecycle.deleted_at"] = None

            if is_active is not None:
                query["is_active"] = bool(is_active)

        docs = list(self.collection.find(query).sort("name", 1))
        return [self.mapper.to_domain(doc) for doc in docs]

    def find_active_default(self):
        doc = self.collection.find_one({
            "lifecycle.deleted_at": None,
            "is_active": True,
        })
        if not doc:
            return None
        return self.mapper.to_domain(doc)