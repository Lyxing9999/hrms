from __future__ import annotations


class ListMyOvertimeRequestsQuery:
    def __init__(self, *, employee_repository, overtime_repository) -> None:
        self.employee_repository = employee_repository
        self.overtime_repository = overtime_repository

    def execute(self, *, user_id, status: str | None = None, page: int = 1, limit: int = 10):
        employee = self.employee_repository.find_by_user_id(user_id)
        if not employee:
            raise ValueError("Employee profile not found")

        return self.overtime_repository.list_requests(
            employee_id=employee["_id"],
            status=status,
            page=page,
            limit=limit,
        )