# app/contexts/hrms/queries/work_location/get_work_location.py
from __future__ import annotations


class GetWorkLocationQuery:
    def __init__(self, *, work_location_repository) -> None:
        self.work_location_repository = work_location_repository

    def execute(self, *, location_id: str):
        return self.work_location_repository.find_by_id(location_id)