from __future__ import annotations


class ApproveLeaveRequestUseCase:
    def __init__(
        self,
        *,
        leave_repository,
        audit_log_repository=None,
    ) -> None:
        self.leave_repository = leave_repository
        self.audit_log_repository = audit_log_repository

    def execute(
        self,
        *,
        leave_request_id: str,
        manager_id: str,
        approved: bool,
        comment: str | None = None,
    ) -> dict:
        leave_request = self._get_leave_request(leave_request_id)

        if approved:
            self._approve(leave_request=leave_request, manager_id=manager_id, comment=comment)
        else:
            self._reject(leave_request=leave_request, manager_id=manager_id, comment=comment)

        self._save_leave_request(leave_request)
        self._write_audit_log(
            leave_request=leave_request,
            manager_id=manager_id,
            approved=approved,
        )

        return self._build_result(leave_request)

    def _get_leave_request(self, leave_request_id: str):
        # TODO
        return self.leave_repository.get_by_id(leave_request_id)

    def _approve(self, *, leave_request, manager_id: str, comment: str | None) -> None:
        # TODO: convert manager_id if needed
        leave_request.approve(manager_id=manager_id, comment=comment)

    def _reject(self, *, leave_request, manager_id: str, comment: str | None) -> None:
        # TODO: convert manager_id if needed
        leave_request.reject(manager_id=manager_id, comment=comment)

    def _save_leave_request(self, leave_request) -> None:
        # TODO
        self.leave_repository.save(leave_request)

    def _write_audit_log(self, *, leave_request, manager_id: str, approved: bool) -> None:
        # TODO
        if self.audit_log_repository is None:
            return

    def _build_result(self, leave_request) -> dict:
        return {
            "leave_request_id": str(leave_request.id),
            "status": leave_request.status.value,
            "manager_comment": leave_request.manager_comment,
        }