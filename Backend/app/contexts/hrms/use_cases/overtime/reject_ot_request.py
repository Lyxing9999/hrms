from __future__ import annotations


class RejectOtRequestUseCase:
    def __init__(
        self,
        *,
        overtime_repository,
        audit_log_repository=None,
    ) -> None:
        self.overtime_repository = overtime_repository
        self.audit_log_repository = audit_log_repository

    def execute(
        self,
        *,
        overtime_request_id: str,
        manager_id: str,
        comment: str | None = None,
    ) -> dict:
        overtime_request = self._get_overtime_request(overtime_request_id)
        self._reject_request(
            overtime_request=overtime_request,
            manager_id=manager_id,
            comment=comment,
        )
        self._save_overtime_request(overtime_request)
        self._write_audit_log(overtime_request=overtime_request, manager_id=manager_id)

        return self._build_result(overtime_request)

    def _get_overtime_request(self, overtime_request_id: str):
        # TODO
        return self.overtime_repository.get_by_id(overtime_request_id)

    def _reject_request(
        self,
        *,
        overtime_request,
        manager_id: str,
        comment: str | None,
    ) -> None:
        # TODO: convert manager_id if needed
        overtime_request.reject(
            manager_id=manager_id,
            comment=comment,
        )

    def _save_overtime_request(self, overtime_request) -> None:
        # TODO
        self.overtime_repository.save(overtime_request)

    def _write_audit_log(self, *, overtime_request, manager_id: str) -> None:
        # TODO
        if self.audit_log_repository is None:
            return

    def _build_result(self, overtime_request) -> dict:
        return {
            "overtime_request_id": str(overtime_request.id),
            "status": overtime_request.status.value,
            "manager_comment": overtime_request.manager_comment,
        }