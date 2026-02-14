# app/contexts/hrms/repositories/employee_repository.py
from typing import Optional
from bson import ObjectId
from pymongo.collection import Collection

from app.contexts.core.errors.mongo_error_mixin import MongoErrorMixin
from app.contexts.shared.lifecycle.filters import not_deleted, by_show_deleted
from app.contexts.shared.lifecycle.domain import now_utc as lifecycle_now_utc
from app.contexts.hrms.mapper.employee_mapper import EmployeeMapper
from app.contexts.hrms.domain.employee import Employee

class MongoEmployeeRepository(MongoErrorMixin):
    def __init__(self, collection: Collection):
        self.collection = collection
        self.mapper = EmployeeMapper()

    def find_one(self, id: ObjectId, *, include_deleted: bool = False) -> Optional[Employee]:
        show = "all" if include_deleted else "active"
        raw = self.collection.find_one(by_show_deleted(show, {"_id": id}))
        return None if not raw else self.mapper.to_domain(raw)

    def save(self, payload: dict) -> Employee:
        res = self.collection.insert_one(dict(payload))
        emp = self.find_one(res.inserted_id)
        if emp is None:
            raise RuntimeError(f"Employee insert ok but load failed: {res.inserted_id}")
        return emp

    def update(self, emp_id: ObjectId, payload: dict) -> Optional[Employee]:
        data = dict(payload)
        data.pop("_id", None)
        data.pop("lifecycle", None)

        res = self.collection.update_one(
            not_deleted({"_id": emp_id}),
            {"$set": {**data, "lifecycle.updated_at": lifecycle_now_utc()}},
        )
        if res.matched_count == 0:
            return None
        return self.find_one(emp_id)