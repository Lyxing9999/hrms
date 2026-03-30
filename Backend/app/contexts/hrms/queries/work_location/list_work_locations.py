# app/contexts/hrms/queries/work_location/list_work_locations.py
from __future__ import annotations


class ListWorkLocationsQuery:
    def __init__(self, *, work_location_repository) -> None:
        self.work_location_repository = work_location_repository

    def execute(self, *, q: str = "", status: str = "all"):
        return self.work_location_repository.list_locations(q=q, status=status)