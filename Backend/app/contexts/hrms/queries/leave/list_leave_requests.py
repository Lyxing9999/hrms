from __future__ import annotations


class ListLeaveRequestsQuery:
    def __init__(self, *, leave_repository) -> None:
        self.leave_repository = leave_repository

    def execute(
        self,
        *,
        employee_id=None,
        status: str | None = None,
        include_deleted: bool = False,
        deleted_only: bool = False,
        page: int = 1,
        page_size: int = 10,
    ):
        return self.leave_repository.list_requests(
            employee_id=employee_id,
            status=status,
            include_deleted=include_deleted,
            deleted_only=deleted_only,
            page=page,
            page_size=page_size,
        )