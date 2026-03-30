# app/contexts/hrms/repositories/work_location_repository.py
from __future__ import annotations

from bson import ObjectId
from pymongo.database import Database

from app.contexts.hrms.mapper.work_location_mapper import WorkLocationMapper


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
            raise ValueError("Work location not found")
        return WorkLocationMapper.to_domain(doc)

    def find_by_id_including_deleted(self, location_id):
        location_id = ObjectId(location_id) if not isinstance(location_id, ObjectId) else location_id
        doc = self.collection.find_one({"_id": location_id})
        if not doc:
            raise ValueError("Work location not found")
        return self.mapper.to_domain(doc)

    def list_locations(
        self,
        *,
        q: str = "",
        status: str = "all",
    ) -> list:
        query: dict = {}

        if q:
            query["$or"] = [
                {"name": {"$regex": q, "$options": "i"}},
                {"address": {"$regex": q, "$options": "i"}},
            ]

        if status == "active":
            query["lifecycle.deleted_at"] = None
            query["is_active"] = True
        elif status == "inactive":
            query["lifecycle.deleted_at"] = None
            query["is_active"] = False
        elif status == "deleted":
            query["lifecycle.deleted_at"] = {"$ne": None}
        else:
            # all
            pass

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