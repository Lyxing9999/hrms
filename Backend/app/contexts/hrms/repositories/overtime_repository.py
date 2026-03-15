from __future__ import annotations

from bson import ObjectId
from datetime import datetime
from pymongo.database import Database

from app.contexts.hrms.domain.overtime import OvertimeRequest
from app.contexts.hrms.mapper.overtime_mapper import OvertimeMapper
from app.contexts.hrms.errors.overtime_exceptions import OvertimeRequestNotFoundException
from app.contexts.shared.time_utils import ensure_utc


class MongoOvertimeRepository:
    def __init__(self, db: Database):
        self.collection = db["hr_overtime_requests"]
        self.mapper = OvertimeMapper()

    def save(self, overtime_request: OvertimeRequest) -> OvertimeRequest:
        doc = self.mapper.to_persistence(overtime_request)
        self.collection.replace_one({"_id": doc["_id"]}, doc, upsert=True)
        return overtime_request

    def find_by_id(self, overtime_request_id: ObjectId) -> OvertimeRequest:
        doc = self.collection.find_one({"_id": overtime_request_id})
        if not doc:
            raise OvertimeRequestNotFoundException(overtime_request_id)
        return self.mapper.to_domain(doc)

    def list_overtime_requests(
        self,
        *,
        employee_id: ObjectId | None = None,
        manager_id: ObjectId | None = None,
        status: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        include_deleted: bool = False,
        deleted_only: bool = False,
        page: int = 1,
        limit: int = 10,
    ) -> tuple[list[OvertimeRequest], int]:
        query = {}

        if employee_id:
            query["employee_id"] = employee_id
        if manager_id:
            query["manager_id"] = manager_id
        if status:
            query["status"] = status

        if start_date or end_date:
            query["request_date"] = {}
            if start_date:
                query["request_date"]["$gte"] = ensure_utc(start_date)
            if end_date:
                query["request_date"]["$lte"] = ensure_utc(end_date)

        if deleted_only:
            query["lifecycle.deleted_at"] = {"$ne": None}
        elif not include_deleted:
            query["lifecycle.deleted_at"] = None

        total = self.collection.count_documents(query)
        skip = (page - 1) * limit

        docs = (
            self.collection.find(query)
            .sort("submitted_at", -1)
            .skip(skip)
            .limit(limit)
        )

        return [self.mapper.to_domain(doc) for doc in docs], total

    def list_approved_by_employee_and_month(
        self,
        *,
        employee_id: ObjectId,
        month: str,
    ) -> list[OvertimeRequest]:
        # TODO: adapt if month is stored differently
        docs = self.collection.find({
            "employee_id": employee_id,
            "status": "approved",
            "month": month,
            "lifecycle.deleted_at": None,
        }).sort("request_date", 1)
        return [self.mapper.to_domain(doc) for doc in docs]

    def find_overlapping_request(
        self,
        *,
        employee_id: ObjectId,
        start_time: datetime,
        end_time: datetime,
    ) -> OvertimeRequest | None:
        start_time = ensure_utc(start_time)
        end_time = ensure_utc(end_time)

        doc = self.collection.find_one({
            "employee_id": employee_id,
            "start_time": {"$lt": end_time},
            "end_time": {"$gt": start_time},
            "lifecycle.deleted_at": None,
        })
        return self.mapper.to_domain(doc) if doc else None

    def delete(self, overtime_request_id: ObjectId) -> None:
        self.collection.delete_one({"_id": overtime_request_id})