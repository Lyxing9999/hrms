# app/contexts/hrms/mapper/working_schedule_mapper.py
from bson import ObjectId
from datetime import time as time_type
from typing import Any

from app.contexts.hrms.domain.working_schedule import WorkingSchedule
from app.contexts.shared.lifecycle.domain import Lifecycle
from app.contexts.shared.lifecycle.dto import LifecycleDTO
from app.contexts.hrms.data_transfer.response.working_schedule_response import WorkingScheduleDTO
from app.contexts.shared.model_converter import mongo_converter


class WorkingScheduleMapper:
    @staticmethod
    def _oid(v) -> ObjectId | None:
        return mongo_converter.convert_to_object_id(v)

    @staticmethod
    def _sid(v) -> str | None:
        if v is None:
            return None
        return str(v)

    @staticmethod
    def _parse_time(v: Any) -> time_type:
        """Parse time from various formats"""
        if isinstance(v, time_type):
            return v
        if isinstance(v, str):
            # Parse "HH:MM:SS" or "HH:MM"
            parts = v.split(":")
            hour = int(parts[0])
            minute = int(parts[1]) if len(parts) > 1 else 0
            second = int(parts[2]) if len(parts) > 2 else 0
            return time_type(hour, minute, second)
        raise ValueError(f"Cannot parse time from {type(v)}: {v}")

    @staticmethod
    def to_domain(data: dict) -> WorkingSchedule:
        if not isinstance(data, dict):
            raise TypeError(f"to_domain expected dict, got {type(data)}")
        
        lc_src = data.get("lifecycle") or {}
        lifecycle = Lifecycle(
            created_at=lc_src.get("created_at") or data.get("created_at"),
            updated_at=lc_src.get("updated_at") or data.get("updated_at"),
            deleted_at=lc_src.get("deleted_at") or data.get("deleted_at"),
            deleted_by=lc_src.get("deleted_by") or data.get("deleted_by"),
        )

        return WorkingSchedule(
            id=WorkingScheduleMapper._oid(data.get("_id") or data.get("id")),
            name=data.get("name") or "",
            start_time=WorkingScheduleMapper._parse_time(data["start_time"]),
            end_time=WorkingScheduleMapper._parse_time(data["end_time"]),
            working_days=data.get("working_days") or [],
            weekend_days=data.get("weekend_days") or [],
            total_hours_per_day=float(data.get("total_hours_per_day", 8.0)),
            is_default=bool(data.get("is_default", False)),
            created_by=WorkingScheduleMapper._oid(data.get("created_by")),
            lifecycle=lifecycle,
        )

    @staticmethod
    def to_persistence(schedule: WorkingSchedule) -> dict:
        if not isinstance(schedule, WorkingSchedule):
            raise TypeError(f"to_persistence expected WorkingSchedule, got {type(schedule)}")
        
        lc = schedule.lifecycle
        doc = {
            "name": schedule.name,
            "start_time": schedule.start_time.strftime("%H:%M:%S"),
            "end_time": schedule.end_time.strftime("%H:%M:%S"),
            "working_days": schedule.working_days,
            "weekend_days": schedule.weekend_days,
            "total_hours_per_day": schedule.total_hours_per_day,
            "is_default": schedule.is_default,
            "created_by": WorkingScheduleMapper._oid(schedule.created_by),
            "lifecycle": {
                "created_at": lc.created_at,
                "updated_at": lc.updated_at,
                "deleted_at": lc.deleted_at,
                "deleted_by": WorkingScheduleMapper._oid(lc.deleted_by),
            },
        }

        if schedule.id:
            doc["_id"] = WorkingScheduleMapper._oid(schedule.id)

        return doc

    @staticmethod
    def to_dto(schedule: WorkingSchedule) -> WorkingScheduleDTO:
        lc = schedule.lifecycle
        return WorkingScheduleDTO(
            id=str(schedule.id),
            name=schedule.name,
            start_time=schedule.start_time,
            end_time=schedule.end_time,
            working_days=schedule.working_days,
            weekend_days=schedule.weekend_days,
            total_hours_per_day=schedule.total_hours_per_day,
            is_default=schedule.is_default,
            created_by=WorkingScheduleMapper._sid(schedule.created_by),
            lifecycle=LifecycleDTO(
                created_at=lc.created_at,
                updated_at=lc.updated_at,
                deleted_at=lc.deleted_at,
                deleted_by=lc.deleted_by,
            ),
        )
