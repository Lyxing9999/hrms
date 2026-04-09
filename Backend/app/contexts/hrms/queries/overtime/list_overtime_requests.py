from __future__ import annotations


class ListOvertimeRequestsQuery:
    def __init__(self, *, overtime_read_model) -> None:
        self.overtime_read_model = overtime_read_model

    def execute(
        self,
        *,
        employee_id: str | None = None,
        status: str | None = None,
        page: int = 1,
        limit: int = 10,
    ):
        return self.overtime_read_model.list_overtime_requests(
            employee_id=employee_id,
            status=status,
            page=page,
            limit=limit,
        )