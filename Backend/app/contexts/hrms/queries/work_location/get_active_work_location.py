# app/contexts/hrms/queries/work_location/get_active_work_location.py
from __future__ import annotations


class GetActiveWorkLocationQuery:
    def __init__(self, *, work_location_repository) -> None:
        self.work_location_repository = work_location_repository

    def execute(self):
        return self.work_location_repository.find_active_default()
    