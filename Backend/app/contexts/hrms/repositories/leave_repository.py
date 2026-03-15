from __future__ import annotations

from bson import ObjectId
from datetime import datetime
from pymongo.database import Database

from app.contexts.hrms.domain.leave import LeaveRequest
from app.contexts.hrms.mapper.leave_mapper import LeaveMapper
from app.contexts.hrms.errors.leave_exceptions import LeaveNotFoundException
from app.contexts.shared.time_utils import ensure_utc


class MongoLeaveRepository:
    def __init__(self, db: Database):
        self.collection = db["hr_leave_requests"]
        self.mapper = LeaveMapper()

    def save(self, leave_request: LeaveRequest) -> LeaveRequest:
        doc = self.mapper.to_persistence(leave_request)
        self.collection.replace_one({"_id": doc["_id"]}, doc, upsert=True)
        return leave_request

    def find_by_id(self, leave_request_id: ObjectId) -> LeaveRequest:
        doc = self.collection.find_one({"_id": leave_request_id})
        if not doc:
            raise LeaveNotFoundException(leave_request_id)
        return self.mapper.to_domain(doc)

    def list_leave_requests(
        self,
        *,
        employee_id: ObjectId | None = None,
        manager_user_id: ObjectId | None = None,
        status: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        include_deleted: bool = False,
        deleted_only: bool = False,
        page: int = 1,
        limit: int = 10,
    ) -> tuple[list[LeaveRequest], int]:
        query = {}

        if employee_id:
            query["employee_id"] = employee_id
        if manager_user_id:
            query["manager_user_id"] = manager_user_id
        if status:
            query["status"] = status

        if start_date or end_date:
            query["start_date"] = {}
            if start_date:
                query["start_date"]["$gte"] = ensure_utc(start_date)
            if end_date:
                query["start_date"]["$lte"] = ensure_utc(end_date)

        if deleted_only:
            query["lifecycle.deleted_at"] = {"$ne": None}
        elif not include_deleted:
            query["lifecycle.deleted_at"] = None

        total = self.collection.count_documents(query)
        skip = (page - 1) * limit

        docs = (
            self.collection.find(query)
            .sort("start_date", -1)
            .skip(skip)
            .limit(limit)
        )

        return [self.mapper.to_domain(doc) for doc in docs], total

    def find_overlapping_leave(
        self,
        *,
        employee_id: ObjectId,
        start_date,
        end_date,
    ) -> LeaveRequest | None:
        doc = self.collection.find_one({
            "employee_id": employee_id,
            "start_date": {"$lte": end_date},
            "end_date": {"$gte": start_date},
            "lifecycle.deleted_at": None,
        })
        return self.mapper.to_domain(doc) if doc else None

    def delete(self, leave_request_id: ObjectId) -> None:
        self.collection.delete_one({"_id": leave_request_id})