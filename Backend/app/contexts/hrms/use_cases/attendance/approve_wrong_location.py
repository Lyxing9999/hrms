from __future__ import annotations

from app.contexts.hrms.domain.audit_log import AuditLog
from app.contexts.hrms.errors.attendance_exceptions import (
    AttendanceNotFoundException,
    AttendanceWrongLocationReviewStateException,
)
from app.contexts.shared.time_utils import utc_now
from app.contexts.shared.model_converter import mongo_converter


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
        attendance_id,
        admin_id,
        approved: bool,
        comment: str | None = None,
        location_id: str | None = None,
    ):
        attendance = self.attendance_repository.find_by_id(attendance_id)
        if not attendance:
            raise AttendanceNotFoundException(attendance_id)

        current_status = (
            attendance.status.value
            if hasattr(attendance.status, "value")
            else str(attendance.status)
        )

        if current_status != "wrong_location_pending":
            raise AttendanceWrongLocationReviewStateException(
                attendance_id=attendance_id,
                current_status=current_status,
            )

        if location_id is not None:
            attendance.location_id = mongo_converter.convert_to_object_id(location_id)

        if approved:
            attendance.approve_wrong_location(
                admin_id=admin_id,
                comment=comment,
            )

            if int(attendance.late_minutes or 0) > 0:
                attendance.status = "late"
            else:
                attendance.status = "checked_in"

            action = "attendance_wrong_location_approved"
        else:
            attendance.reject_wrong_location(
                admin_id=admin_id,
                comment=comment,
            )
            action = "attendance_wrong_location_rejected"

        updated = self.attendance_repository.save(attendance)

        self._write_audit_log(
            action=action,
            actor_id=admin_id,
            entity_id=updated.id,
            details={
                "approved": approved,
                "comment": comment,
                "location_id": location_id,
                "attendance_date": (
                    updated.attendance_date.isoformat()
                    if updated.attendance_date
                    else None
                ),
            },
        )

        return updated

    def _write_audit_log(self, *, action: str, actor_id, entity_id, details: dict) -> None:
        if not self.audit_log_repository:
            return

        audit_log = AuditLog(
            id=None,
            entity_type="attendance",
            entity_id=entity_id,
            action=action,
            actor_id=actor_id,
            action_at=utc_now(),
            details=details,
        )
        self.audit_log_repository.save(audit_log)