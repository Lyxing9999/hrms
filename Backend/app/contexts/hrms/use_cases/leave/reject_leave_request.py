from __future__ import annotations


class RejectLeaveRequestUseCase:
    def __init__(self, *, leave_repository, audit_log_repository=None) -> None:
        self.leave_repository = leave_repository
        self.audit_log_repository = audit_log_repository

    def execute(self, *, leave_id, manager_user_id, comment: str | None = None):
        leave = self.leave_repository.find_by_id(leave_id)
        leave.reject(manager_id=manager_user_id, comment=comment)
        return self.leave_repository.save(leave)