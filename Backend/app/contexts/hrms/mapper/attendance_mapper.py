# app/contexts/hrms/mapper/attendance_mapper.py
from bson import ObjectId
from app.contexts.hrms.domain.attendance import Attendance, AttendanceStatus
from app.contexts.shared.lifecycle.domain import Lifecycle
from app.contexts.shared.lifecycle.dto import LifecycleDTO


class AttendanceMapper:
    @staticmethod
    def to_domain(doc: dict) -> Attendance:
        lifecycle_data = doc.get("lifecycle", {})
        lifecycle = Lifecycle(
            created_at=lifecycle_data.get("created_at"),
            updated_at=lifecycle_data.get("updated_at"),
            deleted_at=lifecycle_data.get("deleted_at"),
            deleted_by=lifecycle_data.get("deleted_by"),
        )

        return Attendance(
            id=doc["_id"],
            employee_id=doc["employee_id"],
            check_in_time=doc["check_in_time"],
            check_out_time=doc.get("check_out_time"),
            location_id=doc.get("location_id"),
            check_in_latitude=doc.get("check_in_latitude"),
            check_in_longitude=doc.get("check_in_longitude"),
            check_out_latitude=doc.get("check_out_latitude"),
            check_out_longitude=doc.get("check_out_longitude"),
            status=doc.get("status", AttendanceStatus.CHECKED_IN),
            notes=doc.get("notes"),
            late_minutes=doc.get("late_minutes", 0),
            early_leave_minutes=doc.get("early_leave_minutes", 0),
            lifecycle=lifecycle,
        )

    @staticmethod
    def to_persistence(attendance: Attendance) -> dict:
        doc = {
            "_id": attendance.id,
            "employee_id": attendance.employee_id,
            "check_in_time": attendance.check_in_time,
            "check_out_time": attendance.check_out_time,
            "location_id": attendance.location_id,
            "check_in_latitude": attendance.check_in_latitude,
            "check_in_longitude": attendance.check_in_longitude,
            "check_out_latitude": attendance.check_out_latitude,
            "check_out_longitude": attendance.check_out_longitude,
            "status": attendance.status.value,
            "notes": attendance.notes,
            "late_minutes": attendance.late_minutes,
            "early_leave_minutes": attendance.early_leave_minutes,
            "lifecycle": {
                "created_at": attendance.lifecycle.created_at,
                "updated_at": attendance.lifecycle.updated_at,
                "deleted_at": attendance.lifecycle.deleted_at,
                "deleted_by": attendance.lifecycle.deleted_by,
            },
        }
        return doc

    @staticmethod
    def to_dto(attendance: Attendance) -> dict:
        return {
            "id": str(attendance.id),
            "employee_id": str(attendance.employee_id),
            "check_in_time": attendance.check_in_time,
            "check_out_time": attendance.check_out_time,
            "location_id": str(attendance.location_id) if attendance.location_id else None,
            "check_in_latitude": attendance.check_in_latitude,
            "check_in_longitude": attendance.check_in_longitude,
            "check_out_latitude": attendance.check_out_latitude,
            "check_out_longitude": attendance.check_out_longitude,
            "status": attendance.status.value,
            "notes": attendance.notes,
            "late_minutes": attendance.late_minutes,
            "early_leave_minutes": attendance.early_leave_minutes,
            "lifecycle": LifecycleDTO(
                created_at=attendance.lifecycle.created_at,
                updated_at=attendance.lifecycle.updated_at,
                deleted_at=attendance.lifecycle.deleted_at,
                deleted_by=str(attendance.lifecycle.deleted_by) if attendance.lifecycle.deleted_by else None,
            ),
        }
