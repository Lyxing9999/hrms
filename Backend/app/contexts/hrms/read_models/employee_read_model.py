from typing import Any, Dict, List, Tuple
from bson import ObjectId
from pymongo.database import Database
from app.contexts.shared.lifecycle.filters import by_show_deleted, ShowDeleted
from app.contexts.shared.model_converter import mongo_converter

class EmployeeReadModel:
    def __init__(self, db: Database):
        self.collection = db["hr_employees"]

    def get_by_id(self, employee_id: ObjectId | str, *, show_deleted: ShowDeleted = "active") -> dict | None:
        oid = mongo_converter.convert_to_object_id(employee_id)
        if not oid:
            return None
        return self.collection.find_one(by_show_deleted(show_deleted, {"_id": oid}))

    def get_by_employee_code(self, employee_code: str, *, show_deleted: ShowDeleted = "active") -> dict | None:
        code = (employee_code or "").strip()
        if not code:
            return None
        return self.collection.find_one(by_show_deleted(show_deleted, {"employee_code": code}))


    def find_employee_by_user_id(self, user_oid):
        return self.collection.find_one({
            "user_id": user_oid,
            "$or": [
                {"lifecycle.deleted_at": None},
                {"lifecycle.deleted_at": {"$exists": False}},
            ]
        })
    def get_page(
        self,
        *,
        page: int = 1,
        page_size: int = 10,
        q: str | None = None,
        show_deleted: ShowDeleted = "active",
    ) -> Tuple[List[dict], int]:
        page = max(1, int(page))
        page_size = min(max(1, int(page_size)), 100)
        skip = (page - 1) * page_size

        base: Dict[str, Any] = {}
        if q and (s := q.strip()):
            base["$or"] = [
                {"employee_code": {"$regex": s, "$options": "i"}},
                {"full_name": {"$regex": s, "$options": "i"}},
                {"department": {"$regex": s, "$options": "i"}},
                {"position": {"$regex": s, "$options": "i"}},
            ]

        query = by_show_deleted(show_deleted, base)
        total = self.collection.count_documents(query)

        items = list(
            self.collection.find(query)
            .sort("lifecycle.created_at", -1)
            .skip(skip)
            .limit(page_size)
        )
        return items, total