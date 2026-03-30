# app/contexts/hrms/use_cases/work_location/deactivate_work_location.py
from __future__ import annotations


class DeactivateWorkLocationUseCase:
    def __init__(self, *, work_location_repository) -> None:
        self.work_location_repository = work_location_repository

    def execute(self, *, location_id: str, actor_id: str):
        location = self.work_location_repository.find_by_id(location_id)
        location.deactivate()
        return self.work_location_repository.save(location)