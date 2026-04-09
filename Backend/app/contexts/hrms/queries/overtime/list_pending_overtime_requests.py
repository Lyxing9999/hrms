from __future__ import annotations


class ListPendingOvertimeRequestsQuery:
    def __init__(self, *, overtime_read_model) -> None:
        self.overtime_read_model = overtime_read_model

    def execute(
        self,
        *,
        employee_id: str | None = None,
        page: int = 1,
        limit: int = 10,
    ):
        return self.overtime_read_model.list_pending_approval(
            employee_id=employee_id,
            page=page,
            limit=limit,
        )