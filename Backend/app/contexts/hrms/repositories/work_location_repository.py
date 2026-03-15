from __future__ import annotations

from bson import ObjectId
from pymongo.database import Database

from app.contexts.hrms.domain.work_location import WorkLocation
from app.contexts.hrms.mapper.work_location_mapper import WorkLocationMapper
from app.contexts.hrms.errors.location_exceptions import WorkLocationNotFoundException


class MongoWorkLocationRepository:
    def __init__(self, db: Database):
        self.collection = db["hr_work_locations"]
        self.mapper = WorkLocationMapper()

    def save(self, location: WorkLocation) -> WorkLocation:
        doc = self.mapper.to_persistence(location)
        self.collection.replace_one({"_id": doc["_id"]}, doc, upsert=True)
        return location

    def find_by_id(self, location_id: ObjectId) -> WorkLocation:
        doc = self.collection.find_one({"_id": location_id})
        if not doc:
            raise WorkLocationNotFoundException(location_id)
        return self.mapper.to_domain(doc)

    def find_active_default(self) -> WorkLocation | None:
        # TODO: if your schema has `is_default`
        doc = self.collection.find_one({
            "is_active": True,
            "lifecycle.deleted_at": None,
        })
        return self.mapper.to_domain(doc) if doc else None

    def list_locations(
        self,
        *,
        is_active: bool | None = None,
        include_deleted: bool = False,
        deleted_only: bool = False,
    ) -> list[WorkLocation]:
        query = {}

        if is_active is not None:
            query["is_active"] = is_active

        if deleted_only:
            query["lifecycle.deleted_at"] = {"$ne": None}
        elif not include_deleted:
            query["lifecycle.deleted_at"] = None

        docs = self.collection.find(query).sort("name", 1)
        return [self.mapper.to_domain(doc) for doc in docs]

    def delete(self, location_id: ObjectId) -> None:
        self.collection.delete_one({"_id": location_id})