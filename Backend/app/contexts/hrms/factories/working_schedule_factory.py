# app/contexts/hrms/factories/working_schedule_factory.py
from bson import ObjectId
from datetime import time as time_type

from app.contexts.hrms.domain.working_schedule import WorkingSchedule


class WorkingScheduleFactory:
    def __init__(self, schedule_read_model):
        self._read = schedule_read_model

    def create_schedule(self, *, payload: dict, created_by: str | ObjectId | None) -> WorkingSchedule:
        name = (payload.get("name") or "").strip()
        
        # Check if name already exists
        existing = self._read.get_by_name(name)
        if existing:
            raise ValueError(f"Working schedule with name '{name}' already exists")
        
        return WorkingSchedule(
            name=name,
            start_time=payload["start_time"],
            end_time=payload["end_time"],
            working_days=payload["working_days"],
            is_default=payload.get("is_default", False),
            created_by=created_by,
        )
