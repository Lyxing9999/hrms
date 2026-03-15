from __future__ import annotations

from bson import ObjectId
from pymongo.database import Database

from app.contexts.hrms.domain.working_schedule import WorkingSchedule
from app.contexts.hrms.mapper.working_schedule_mapper import WorkingScheduleMapper
from app.contexts.hrms.errors.schedule_exceptions import WorkingScheduleNotFoundException


class MongoWorkingScheduleRepository:
    def __init__(self, db: Database):
        self.collection = db["hr_working_schedules"]
        self.mapper = WorkingScheduleMapper()

    def save(self, schedule: WorkingSchedule) -> WorkingSchedule:
        doc = self.mapper.to_persistence(schedule)
        self.collection.replace_one({"_id": doc["_id"]}, doc, upsert=True)
        return schedule

    def find_by_id(self, schedule_id: ObjectId) -> WorkingSchedule:
        doc = self.collection.find_one({"_id": schedule_id})
        if not doc:
            raise WorkingScheduleNotFoundException(schedule_id)
        return self.mapper.to_domain(doc)

    def find_default(self) -> WorkingSchedule | None:
        doc = self.collection.find_one({
            "is_default": True,
            "lifecycle.deleted_at": None,
        })
        return self.mapper.to_domain(doc) if doc else None

    def list_schedules(
        self,
        *,
        is_default: bool | None = None,
        include_deleted: bool = False,
        deleted_only: bool = False,
    ) -> list[WorkingSchedule]:
        query = {}

        if is_default is not None:
            query["is_default"] = is_default

        if deleted_only:
            query["lifecycle.deleted_at"] = {"$ne": None}
        elif not include_deleted:
            query["lifecycle.deleted_at"] = None

        docs = self.collection.find(query).sort("name", 1)
        return [self.mapper.to_domain(doc) for doc in docs]

    def delete(self, schedule_id: ObjectId) -> None:
        self.collection.delete_one({"_id": schedule_id})