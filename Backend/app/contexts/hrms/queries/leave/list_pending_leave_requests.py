from __future__ import annotations


class ListPendingLeaveRequestsQuery:
    def __init__(self, *, leave_repository) -> None:
        self.leave_repository = leave_repository

    def execute(self, *, page: int = 1, page_size: int = 10):
        return self.leave_repository.list_requests(
            status="pending",
            page=page,
            page_size=page_size,
        )