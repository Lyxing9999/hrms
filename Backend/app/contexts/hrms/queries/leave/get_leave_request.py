from __future__ import annotations


class GetLeaveRequestQuery:
    def __init__(self, *, leave_repository) -> None:
        self.leave_repository = leave_repository

    def execute(self, *, leave_id):
        return self.leave_repository.find_by_id(leave_id)