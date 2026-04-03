from __future__ import annotations

from datetime import datetime, timezone

from app.contexts.hrms.errors.attendance_exceptions import (
    AttendanceNotFoundException,
    AttendanceWrongLocationReviewStateException,
)


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
    ) -> dict:
        attendance = self.attendance_repository.find_by_id(attendance_id)
        if not attendance:
            raise AttendanceNotFoundException(attendance_id)

        current_status = str(attendance.get("status") or "unknown")
        if current_status != "wrong_location_pending":
            raise AttendanceWrongLocationReviewStateException(
                attendance_id=attendance_id,
                current_status=current_status,
            )

        if approved:
            new_status = "late" if attendance.get("late_minutes", 0) > 0 else "checked_in"
            action = "attendance_wrong_location_approved"
        else:
            new_status = "wrong_location_rejected"
            action = "attendance_wrong_location_rejected"

        updated = self.attendance_repository.update_fields(
            attendance["_id"],
            {
                "status": new_status,
                "admin_comment": comment,
                "location_reviewed_by": admin_id,
                "lifecycle.updated_at": datetime.now(timezone.utc),
            },
        )

        self._write_audit_log(
            action=action,
            actor_id=admin_id,
            entity_id=updated["_id"],
            details={
                "approved": approved,
                "comment": comment,
                "attendance_date": str(updated["attendance_date"]),
            },
        )

        return updated

    def _write_audit_log(self, *, action: str, actor_id, entity_id, details: dict) -> None:
        if not self.audit_log_repository:
            return

        self.audit_log_repository.save(
            {
                "entity_type": "attendance",
                "entity_id": entity_id,
                "action": action,
                "actor_id": actor_id,
                "action_at": datetime.now(timezone.utc),
                "details": details,
            }
        )