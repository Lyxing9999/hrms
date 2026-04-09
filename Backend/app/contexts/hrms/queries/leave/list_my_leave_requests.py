from __future__ import annotations


class ListMyLeaveRequestsQuery:
    def __init__(self, *, leave_repository) -> None:
        self.leave_repository = leave_repository

    def execute(
        self,
        *,
        employee_id,
        status: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ):
        return self.leave_repository.list_requests(
            employee_id=employee_id,
            status=status,
            page=page,
            page_size=page_size,
        )