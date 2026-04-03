from __future__ import annotations


class ListOvertimeRequestsQuery:
    def __init__(self, *, overtime_repository) -> None:
        self.overtime_repository = overtime_repository

    def execute(
        self,
        *,
        employee_id=None,
        status: str | None = None,
        page: int = 1,
        limit: int = 10,
    ):
        return self.overtime_repository.list_requests(
            employee_id=employee_id,
            status=status,
            page=page,
            limit=limit,
        )