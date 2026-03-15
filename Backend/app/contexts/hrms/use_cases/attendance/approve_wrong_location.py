from __future__ import annotations


class ApproveWrongLocationUseCase:
    def __init__(
        self,
        *,
        attendance_repository,
        audit_log_repository=None,
    ) -> None:
        self.attendance_repository = attendance_repository
        self.audit_log_repository = audit_log_repository

    def execute(
        self,
        *,
        attendance_id: str,
        admin_id: str,
        approved: bool,
        comment: str | None = None,
    ) -> dict:
        attendance = self._get_attendance(attendance_id)
        self._ensure_pending_wrong_location(attendance)

        if approved:
            self._approve(attendance=attendance, admin_id=admin_id, comment=comment)
        else:
            self._reject(attendance=attendance, admin_id=admin_id, comment=comment)

        self._save_attendance(attendance)
        self._write_audit_log(attendance=attendance, admin_id=admin_id, approved=approved)

        return self._build_result(attendance)

    def _get_attendance(self, attendance_id: str):
        # TODO
        return self.attendance_repository.get_by_id(attendance_id)

    def _ensure_pending_wrong_location(self, attendance) -> None:
        # TODO: validate current status is WRONG_LOCATION_PENDING
        pass

    def _approve(self, *, attendance, admin_id: str, comment: str | None) -> None:
        # TODO: convert admin_id if needed
        attendance.approve_wrong_location(
            admin_id=admin_id,
            comment=comment,
        )

    def _reject(self, *, attendance, admin_id: str, comment: str | None) -> None:
        # TODO: convert admin_id if needed
        attendance.reject_wrong_location(
            admin_id=admin_id,
            comment=comment,
        )

    def _save_attendance(self, attendance) -> None:
        # TODO
        self.attendance_repository.save(attendance)

    def _write_audit_log(self, *, attendance, admin_id: str, approved: bool) -> None:
        # TODO
        if self.audit_log_repository is None:
            return

    def _build_result(self, attendance) -> dict:
        return {
            "attendance_id": str(attendance.id),
            "status": attendance.status.value,
            "admin_comment": attendance.admin_comment,
        }