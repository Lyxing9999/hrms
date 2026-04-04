from __future__ import annotations

from bson import ObjectId
from pymongo.database import Database

from app.contexts.shared.model_converter import mongo_converter
from pymongo import ReturnDocument



class MongoEmployeeRepository:
    def __init__(self, db: Database):
        self.collection = db["hr_employees"]
    @staticmethod
    def _oid(v) -> ObjectId | None:
        return mongo_converter.convert_to_object_id(v)

    @staticmethod
    def _sid(v) -> str | None:
        if v is None:
            return None
        return str(v)
    
    def create(self, doc: dict) -> dict:
        result = self.collection.insert_one(doc)
        return self.find_by_id(result.inserted_id)

    def save(self, doc: dict) -> dict:
        self.collection.replace_one({"_id": self._oid(doc["_id"])}, doc, upsert=True)
        return self.find_by_id(doc["_id"])

    def find_by_id(self, employee_id) -> dict:
        employee_id = self._oid(employee_id) if not isinstance(employee_id, ObjectId) else employee_id
        doc = self.collection.find_one({
            "_id": employee_id,
            "lifecycle.deleted_at": None,
        })
        if not doc:
            raise ValueError("Employee not found")
        return doc

    def find_by_id_including_deleted(self, employee_id) -> dict:
        employee_id = self._oid(employee_id) if not isinstance(employee_id, ObjectId) else employee_id
        doc = self.collection.find_one({"_id": employee_id})
        if not doc:
            raise ValueError("Employee not found")
        return doc

    def find_by_user_id(self, user_id) -> dict | None:
        user_id = self._oid(user_id) if not isinstance(user_id, ObjectId) else user_id
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
        employee_id = self._oid(employee_id) if not isinstance(employee_id, ObjectId) else employee_id
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
    

    def create_with_session(self, doc: dict, session=None) -> dict:
        result = self.collection.insert_one(doc, session=session)
        return self.collection.find_one({"_id": result.inserted_id}, session=session)


    def link_user_if_empty_with_session(self, *, employee_id, user_id, session=None) -> dict | None:
        employee_oid = self._oid(employee_id)
        user_oid = self._oid(user_id)

        return self.collection.find_one_and_update(
            {
                "_id": employee_oid,
                "user_id": None,
                "lifecycle.deleted_at": None,
            },
            {
                "$set": {
                    "user_id": user_oid,
                }
            },
            session=session,
            return_document=ReturnDocument.AFTER,
        )