from __future__ import annotations


class ListWorkingSchedulesQuery:
    def __init__(self, *, working_schedule_repository) -> None:
        self.working_schedule_repository = working_schedule_repository

    def execute(
        self,
        *,
        page: int = 1,
        page_size: int = 10,
        include_deleted: bool = False,
        deleted_only: bool = False,
    ):
        # Note: Pagination is handled on the frontend.
        # The repository returns all matching schedules without pagination.
        return self.working_schedule_repository.list_schedules(
            include_deleted=include_deleted,
            deleted_only=deleted_only,
        )