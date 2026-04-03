from __future__ import annotations

from bson import ObjectId

from app.contexts.hrms.domain.attendance import Attendance, AttendanceStatus, ReviewStatus
from app.contexts.shared.lifecycle.domain import Lifecycle
from app.contexts.shared.lifecycle.dto import LifecycleDTO
from app.contexts.hrms.data_transfer.response.attendance_response import AttendanceDTO
from app.contexts.shared.model_converter import mongo_converter


class AttendanceMapper:
    @staticmethod
    def _oid(v) -> ObjectId | None:
        return mongo_converter.convert_to_object_id(v)

    @staticmethod
    def _sid(v) -> str | None:
        if v is None:
            return None
        return str(v)

    @staticmethod
    def to_domain(data: dict) -> Attendance:
        if not isinstance(data, dict):
            raise TypeError(f"to_domain expected dict, got {type(data)}")

        lc_src = data.get("lifecycle") or {}
        lifecycle = Lifecycle(
            created_at=lc_src.get("created_at") or data.get("created_at"),
            updated_at=lc_src.get("updated_at") or data.get("updated_at"),
            deleted_at=lc_src.get("deleted_at") or data.get("deleted_at"),
            deleted_by=lc_src.get("deleted_by") or data.get("deleted_by"),
        )

        return Attendance(
            id=AttendanceMapper._oid(data.get("_id") or data.get("id")),
            employee_id=AttendanceMapper._oid(data.get("employee_id")),
            attendance_date=data.get("attendance_date"),
            check_in_time=data.get("check_in_time"),
            check_out_time=data.get("check_out_time"),
            schedule_id=AttendanceMapper._oid(data.get("schedule_id")),
            location_id=AttendanceMapper._oid(data.get("location_id")),
            check_in_latitude=data.get("check_in_latitude"),
            check_in_longitude=data.get("check_in_longitude"),
            check_out_latitude=data.get("check_out_latitude"),
            check_out_longitude=data.get("check_out_longitude"),
            day_type=data.get("day_type", "working_day"),
            is_ot_eligible=bool(data.get("is_ot_eligible", False)),
            status=data.get("status", AttendanceStatus.CHECKED_IN.value),
            notes=data.get("notes"),
            late_minutes=int(data.get("late_minutes", 0)),
            early_leave_minutes=int(data.get("early_leave_minutes", 0)),
            wrong_location_reason=data.get("wrong_location_reason"),
            late_reason=data.get("late_reason"),
            early_leave_reason=data.get("early_leave_reason"),
            early_leave_review_status=data.get(
                "early_leave_review_status",
                ReviewStatus.NOT_REQUIRED.value,
            ),
            admin_comment=data.get("admin_comment"),
            location_reviewed_by=AttendanceMapper._oid(data.get("location_reviewed_by")),
            early_leave_reviewed_by=AttendanceMapper._oid(data.get("early_leave_reviewed_by")),
            lifecycle=lifecycle,
        )

    @staticmethod
    def to_persistence(attendance: Attendance) -> dict:
        if not isinstance(attendance, Attendance):
            raise TypeError(f"to_persistence expected Attendance, got {type(attendance)}")

        lc = attendance.lifecycle
        doc = {
            "employee_id": AttendanceMapper._oid(attendance.employee_id),
            "attendance_date": attendance.attendance_date,
            "check_in_time": attendance.check_in_time,
            "check_out_time": attendance.check_out_time,
            "schedule_id": AttendanceMapper._oid(attendance.schedule_id),
            "location_id": AttendanceMapper._oid(attendance.location_id),
            "check_in_latitude": attendance.check_in_latitude,
            "check_in_longitude": attendance.check_in_longitude,
            "check_out_latitude": attendance.check_out_latitude,
            "check_out_longitude": attendance.check_out_longitude,
            "status": attendance.status.value if hasattr(attendance.status, "value") else str(attendance.status),
            "notes": attendance.notes,
            "late_minutes": attendance.late_minutes,
            "early_leave_minutes": attendance.early_leave_minutes,
            "wrong_location_reason": attendance.wrong_location_reason,
            "day_type": attendance.day_type.value if hasattr(attendance.day_type, "value") else str(attendance.day_type),
            "is_ot_eligible": attendance.is_ot_eligible,
            "late_reason": attendance.late_reason,
            "early_leave_reason": attendance.early_leave_reason,
            "early_leave_review_status": (
                attendance.early_leave_review_status.value
                if hasattr(attendance.early_leave_review_status, "value")
                else str(attendance.early_leave_review_status)
            ),
            "admin_comment": attendance.admin_comment,
            "location_reviewed_by": AttendanceMapper._oid(attendance.location_reviewed_by),
            "early_leave_reviewed_by": AttendanceMapper._oid(attendance.early_leave_reviewed_by),
            "lifecycle": {
                "created_at": lc.created_at,
                "updated_at": lc.updated_at,
                "deleted_at": lc.deleted_at,
                "deleted_by": AttendanceMapper._oid(lc.deleted_by),
            },
        }

        if attendance.id:
            doc["_id"] = AttendanceMapper._oid(attendance.id)

        return doc

    @staticmethod
    def to_dto(attendance: Attendance) -> AttendanceDTO:
        lc = attendance.lifecycle
        return AttendanceDTO(
            id=str(attendance.id),
            employee_id=AttendanceMapper._sid(attendance.employee_id),
            attendance_date=attendance.attendance_date,
            check_in_time=attendance.check_in_time,
            check_out_time=attendance.check_out_time,
            schedule_id=AttendanceMapper._sid(attendance.schedule_id),
            location_id=AttendanceMapper._sid(attendance.location_id),
            check_in_latitude=attendance.check_in_latitude,
            check_in_longitude=attendance.check_in_longitude,
            check_out_latitude=attendance.check_out_latitude,
            check_out_longitude=attendance.check_out_longitude,
            day_type=attendance.day_type.value if hasattr(attendance.day_type, "value") else str(attendance.day_type),
            is_ot_eligible=attendance.is_ot_eligible,        
            status=attendance.status.value if hasattr(attendance.status, "value") else str(attendance.status),
            notes=attendance.notes,
            late_minutes=attendance.late_minutes,
            early_leave_minutes=attendance.early_leave_minutes,
            wrong_location_reason=attendance.wrong_location_reason,
            late_reason=attendance.late_reason,
            early_leave_reason=attendance.early_leave_reason,
            early_leave_review_status=(
                attendance.early_leave_review_status.value
                if hasattr(attendance.early_leave_review_status, "value")
                else str(attendance.early_leave_review_status)
            ),
            admin_comment=attendance.admin_comment,
            location_reviewed_by=AttendanceMapper._sid(attendance.location_reviewed_by),
            early_leave_reviewed_by=AttendanceMapper._sid(attendance.early_leave_reviewed_by),
            lifecycle=LifecycleDTO(
                created_at=lc.created_at,
                updated_at=lc.updated_at,
                deleted_at=lc.deleted_at,
                deleted_by=AttendanceMapper._sid(lc.deleted_by),
            ),
        )