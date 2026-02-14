# app/contexts/hrms/services/working_schedule_service.py
from __future__ import annotations
from bson import ObjectId
from pymongo.database import Database

from app.contexts.hrms.read_models.working_schedule_read_model import WorkingScheduleReadModel
from app.contexts.hrms.repositories.working_schedule_repository import MongoWorkingScheduleRepository
from app.contexts.hrms.factories.working_schedule_factory import WorkingScheduleFactory
from app.contexts.hrms.mapper.working_schedule_mapper import WorkingScheduleMapper
from app.contexts.hrms.domain.working_schedule import WorkingSchedule
from app.contexts.shared.lifecycle.filters import ShowDeleted
from app.contexts.shared.lifecycle.domain import now_utc
from app.contexts.shared.model_converter import mongo_converter


class WorkingScheduleNotFoundException(Exception):
    def __init__(self, schedule_id: str):
        super().__init__(f"Working schedule not found: {schedule_id}")


class WorkingScheduleService:
    def __init__(self, db: Database):
        self.db = db
        self._read = WorkingScheduleReadModel(db)
        self._repo = MongoWorkingScheduleRepository(db["working_schedules"])
        self._mapper = WorkingScheduleMapper()
        self._factory = WorkingScheduleFactory(self._read)

    def _oid(self, v: str | ObjectId | None) -> ObjectId | None:
        return mongo_converter.convert_to_object_id(v)

    # -------------------------
    # LIST
    # -------------------------
    def list_schedules(
        self,
        *,
        q: str = "",
        page: int = 1,
        page_size: int = 10,
        show_deleted: ShowDeleted = "active",
    ) -> tuple[list[WorkingSchedule], int]:
        items, total = self._read.get_page(
            page=page,
            page_size=page_size,
            q=q,
            show_deleted=show_deleted,
        )
        domains = [self._mapper.to_domain(x) for x in items]
        return domains, int(total)

    # -------------------------
    # GET ONE
    # -------------------------
    def get_schedule(self, schedule_id: str | ObjectId, *, show_deleted: ShowDeleted = "active") -> WorkingSchedule:
        raw = self._read.get_by_id(self._oid(schedule_id), show_deleted=show_deleted)
        if not raw:
            raise WorkingScheduleNotFoundException(str(schedule_id))
        return self._mapper.to_domain(raw)

    # -------------------------
    # GET DEFAULT
    # -------------------------
    def get_default_schedule(self) -> WorkingSchedule | None:
        raw = self._read.get_default(show_deleted="active")
        if not raw:
            return None
        return self._mapper.to_domain(raw)

    # -------------------------
    # CREATE
    # -------------------------
    def create_schedule(self, payload, *, created_by_user_id: str | ObjectId) -> WorkingSchedule:
        actor_oid = self._oid(created_by_user_id)
        
        p = payload.model_dump()
        
        # If this is set as default, unset other defaults first
        if p.get("is_default", False):
            self._unset_all_defaults()
        
        schedule = self._factory.create_schedule(payload=p, created_by=actor_oid)
        saved = self._repo.save(self._mapper.to_persistence(schedule))
        
        return saved

    # -------------------------
    # UPDATE
    # -------------------------
    def update_schedule(self, schedule_id: str | ObjectId, payload, *, actor_id: str | ObjectId) -> WorkingSchedule:
        schedule = self.get_schedule(schedule_id, show_deleted="active")
        
        p = payload.model_dump(exclude_unset=True)
        
        # Update fields
        if "name" in p and p["name"]:
            # Check if new name conflicts with existing
            existing = self._read.get_by_name(p["name"])
            if existing and str(existing["_id"]) != str(schedule.id):
                raise ValueError(f"Working schedule with name '{p['name']}' already exists")
            schedule.name = str(p["name"]).strip()
        
        if "start_time" in p and "end_time" in p:
            schedule.update_times(p["start_time"], p["end_time"])
        elif "start_time" in p or "end_time" in p:
            # If only one is provided, use current value for the other
            start = p.get("start_time", schedule.start_time)
            end = p.get("end_time", schedule.end_time)
            schedule.update_times(start, end)
        
        if "working_days" in p and p["working_days"]:
            schedule.update_working_days(p["working_days"])
        
        if "is_default" in p and p["is_default"]:
            self._unset_all_defaults()
            schedule.set_as_default()
        
        schedule.lifecycle.touch(now_utc())
        
        updated = self._repo.update(self._oid(schedule.id), self._mapper.to_persistence(schedule))
        if not updated:
            raise WorkingScheduleNotFoundException(str(schedule_id))
        
        return updated

    # -------------------------
    # SOFT DELETE
    # -------------------------
    def soft_delete_schedule(self, schedule_id: str | ObjectId, *, actor_id: str | ObjectId) -> WorkingSchedule:
        schedule = self.get_schedule(schedule_id, show_deleted="active")
        
        # Don't allow deleting default schedule
        if schedule.is_default:
            raise ValueError("Cannot delete the default working schedule")
        
        schedule.soft_delete(actor_id=actor_id)
        
        updated = self._repo.update(self._oid(schedule.id), self._mapper.to_persistence(schedule))
        if not updated:
            raise WorkingScheduleNotFoundException(str(schedule_id))
        
        return updated

    # -------------------------
    # RESTORE
    # -------------------------
    def restore_schedule(self, schedule_id: str | ObjectId) -> WorkingSchedule:
        schedule = self.get_schedule(schedule_id, show_deleted="deleted_only")
        
        schedule.lifecycle.restore()
        
        updated = self._repo.update(self._oid(schedule.id), self._mapper.to_persistence(schedule))
        if not updated:
            raise WorkingScheduleNotFoundException(str(schedule_id))
        
        return updated

    # -------------------------
    # HELPER: Unset all defaults
    # -------------------------
    def _unset_all_defaults(self):
        """Unset is_default flag for all schedules"""
        self.db["working_schedules"].update_many(
            {"is_default": True},
            {"$set": {"is_default": False}}
        )
