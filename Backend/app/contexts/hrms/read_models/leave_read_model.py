# app/contexts/hrms/read_models/leave_read_model.py
from typing import Tuple, List, Dict, Any
from bson import ObjectId
from pymongo.database import Database
from app.contexts.shared.lifecycle.filters import by_show_deleted, ShowDeleted
from app.contexts.shared.model_converter import mongo_converter

class LeaveReadModel:
    def __init__(self, db: Database):
        self.collection = db["leave_requests"]

    def get_by_id(self, leave_id: ObjectId | str, *, show_deleted: ShowDeleted = "active") -> dict | None:
        oid = mongo_converter.convert_to_object_id(leave_id)
        if not oid:
            return None
        return self.collection.find_one(by_show_deleted(show_deleted, {"_id": oid}))

    def get_page(
        self,
        *,
        page: int = 1,
        page_size: int = 10,
        q: str = "",
        employee_id: str | None = None,
        status: str | None = None,
        show_deleted: ShowDeleted = "active",
    ) -> Tuple[List[Dict[str, Any]], int]:
        query = by_show_deleted(show_deleted, {})
        
        # Filter by employee
        if employee_id:
            emp_oid = mongo_converter.convert_to_object_id(employee_id)
            if emp_oid:
                query["employee_id"] = emp_oid
        
        # Filter by status
        if status:
            query["status"] = status.lower()
        
        # Search in reason
        if q:
            query["reason"] = {"$regex": q, "$options": "i"}
        
        total = self.collection.count_documents(query)
        
        skip = (page - 1) * page_size
        items = list(
            self.collection.find(query)
            .sort("lifecycle.created_at", -1)
            .skip(skip)
            .limit(page_size)
        )
        
        return items, total
