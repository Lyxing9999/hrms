# app/contexts/hrms/queries/work_location/list_work_locations.py
from __future__ import annotations


class ListWorkLocationsQuery:
    def __init__(self, *, work_location_repository) -> None:
        self.work_location_repository = work_location_repository

    def execute(
        self,
        *,
        q: str = "",
        status: str = "all",
        include_deleted: bool | None = None,
        deleted_only: bool | None = None,
        is_active: bool | None = None,
    ):
        return self.work_location_repository.list_locations(
            q=q,
            status=status,
            include_deleted=include_deleted,
            deleted_only=deleted_only,
            is_active=is_active,
        )