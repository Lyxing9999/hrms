from __future__ import annotations

from bson import ObjectId
from pymongo.database import Database


class MongoEmployeeRepository:
    def __init__(self, db: Database):
        self.collection = db["hr_employees"]

    def create(self, doc: dict) -> dict:
        result = self.collection.insert_one(doc)
        return self.find_by_id(result.inserted_id)

    def save(self, doc: dict) -> dict:
        self.collection.replace_one({"_id": doc["_id"]}, doc, upsert=True)
        return self.find_by_id(doc["_id"])

    def find_by_id(self, employee_id) -> dict:
        employee_id = ObjectId(employee_id) if not isinstance(employee_id, ObjectId) else employee_id
        doc = self.collection.find_one({
            "_id": employee_id,
            "lifecycle.deleted_at": None,
        })
        if not doc:
            raise ValueError("Employee not found")
        return doc

    def find_by_id_including_deleted(self, employee_id) -> dict:
        employee_id = ObjectId(employee_id) if not isinstance(employee_id, ObjectId) else employee_id
        doc = self.collection.find_one({"_id": employee_id})
        if not doc:
            raise ValueError("Employee not found")
        return doc

    def find_by_user_id(self, user_id) -> dict | None:
        user_id = ObjectId(user_id) if not isinstance(user_id, ObjectId) else user_id
        return self.collection.find_one({
            "user_id": user_id,
            "lifecycle.deleted_at": None,
        })

    def find_by_employee_code(self, employee_code: str) -> dict | None:
        return self.collection.find_one({
            "employee_code": employee_code,
            "lifecycle.deleted_at": None,
        })

    def update_fields(self, employee_id, fields: dict) -> dict:
        employee_id = ObjectId(employee_id) if not isinstance(employee_id, ObjectId) else employee_id
        self.collection.update_one({"_id": employee_id}, {"$set": fields})
        return self.find_by_id_including_deleted(employee_id)

    def list_employees(
        self,
        *,
        q: str = "",
        page: int = 1,
        page_size: int = 10,
        show_deleted: str = "active",
    ) -> tuple[list[dict], int]:
        query = {}

        if q:
            query["$or"] = [
                {"employee_code": {"$regex": q, "$options": "i"}},
                {"full_name": {"$regex": q, "$options": "i"}},
                {"department": {"$regex": q, "$options": "i"}},
                {"position": {"$regex": q, "$options": "i"}},
            ]

        if show_deleted == "active":
            query["lifecycle.deleted_at"] = None
        elif show_deleted == "deleted_only":
            query["lifecycle.deleted_at"] = {"$ne": None}

        total = self.collection.count_documents(query)
        skip = (page - 1) * page_size

        items = list(
            self.collection.find(query)
            .sort("employee_code", 1)
            .skip(skip)
            .limit(page_size)
        )

        return items, total