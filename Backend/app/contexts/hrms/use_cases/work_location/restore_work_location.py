# app/contexts/hrms/use_cases/work_location/restore_work_location.py
from __future__ import annotations

from app.contexts.shared.lifecycle.domain import now_utc


class RestoreWorkLocationUseCase:
    def __init__(self, *, work_location_repository) -> None:
        self.work_location_repository = work_location_repository

    def execute(self, *, location_id: str):
        location = self.work_location_repository.find_by_id_including_deleted(location_id)
        location.lifecycle.deleted_at = None
        location.lifecycle.deleted_by = None
        location.lifecycle.touch(now_utc())
        return self.work_location_repository.save(location)