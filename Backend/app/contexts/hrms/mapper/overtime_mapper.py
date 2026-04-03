from __future__ import annotations

from bson import ObjectId

from app.contexts.hrms.domain.overtime import OvertimeRequest
from app.contexts.hrms.data_transfer.response.overtime_response import OvertimeDTO
from app.contexts.shared.lifecycle.domain import Lifecycle
from app.contexts.shared.lifecycle.dto import LifecycleDTO
from app.contexts.shared.model_converter import mongo_converter


class OvertimeMapper:
    @staticmethod
    def _oid(v) -> ObjectId | None:
        return mongo_converter.convert_to_object_id(v)

    @staticmethod
    def _sid(v) -> str | None:
        if v is None:
            return None
        return str(v)

    @staticmethod
    def to_domain(data: dict) -> OvertimeRequest:
        lc_src = data.get("lifecycle") or {}
        lifecycle = Lifecycle(
            created_at=lc_src.get("created_at") or data.get("created_at"),
            updated_at=lc_src.get("updated_at") or data.get("updated_at"),
            deleted_at=lc_src.get("deleted_at") or data.get("deleted_at"),
            deleted_by=lc_src.get("deleted_by") or data.get("deleted_by"),
        )

        return OvertimeRequest(
            id=OvertimeMapper._oid(data.get("_id") or data.get("id")),
            employee_id=OvertimeMapper._oid(data.get("employee_id")),
            request_date=data.get("request_date"),
            start_time=data.get("start_time"),
            end_time=data.get("end_time"),
            schedule_end_time=data.get("schedule_end_time"),
            reason=data.get("reason"),
            day_type=data.get("day_type"),
            basic_salary=float(data.get("basic_salary", 0)),
            submitted_at=data.get("submitted_at"),
            status=data.get("status"),
            manager_id=OvertimeMapper._oid(data.get("manager_id")),
            manager_comment=data.get("manager_comment"),
            approved_hours=float(data.get("approved_hours", 0)),
            calculated_payment=float(data.get("calculated_payment", 0)),
            lifecycle=lifecycle,
        )

    @staticmethod
    def to_persistence(ot: OvertimeRequest) -> dict:
        lc = ot.lifecycle
        doc = {
            "employee_id": OvertimeMapper._oid(ot.employee_id),
            "request_date": ot.request_date,
            "start_time": ot.start_time,
            "end_time": ot.end_time,
            "schedule_end_time": ot.schedule_end_time,
            "reason": ot.reason,
            "day_type": ot.day_type.value if hasattr(ot.day_type, "value") else str(ot.day_type),
            "basic_salary": ot.basic_salary,
            "submitted_at": ot.submitted_at,
            "status": ot.status.value if hasattr(ot.status, "value") else str(ot.status),
            "manager_id": OvertimeMapper._oid(ot.manager_id),
            "manager_comment": ot.manager_comment,
            "approved_hours": ot.approved_hours,
            "calculated_payment": ot.calculated_payment,
            "lifecycle": {
                "created_at": lc.created_at,
                "updated_at": lc.updated_at,
                "deleted_at": lc.deleted_at,
                "deleted_by": OvertimeMapper._oid(lc.deleted_by),
            },
        }

        if ot.id:
            doc["_id"] = OvertimeMapper._oid(ot.id)

        return doc

    @staticmethod
    def to_dto(ot: OvertimeRequest) -> OvertimeDTO:
        lc = ot.lifecycle
        return OvertimeDTO(
            id=str(ot.id),
            employee_id=OvertimeMapper._sid(ot.employee_id),
            request_date=ot.request_date,
            start_time=ot.start_time,
            end_time=ot.end_time,
            schedule_end_time=ot.schedule_end_time,
            reason=ot.reason,
            day_type=ot.day_type.value if hasattr(ot.day_type, "value") else str(ot.day_type),
            basic_salary=ot.basic_salary,
            submitted_at=ot.submitted_at,
            status=ot.status.value if hasattr(ot.status, "value") else str(ot.status),
            manager_id=OvertimeMapper._sid(ot.manager_id),
            manager_comment=ot.manager_comment,
            approved_hours=ot.approved_hours,
            calculated_payment=ot.calculated_payment,
            lifecycle=LifecycleDTO(
                created_at=lc.created_at,
                updated_at=lc.updated_at,
                deleted_at=lc.deleted_at,
                deleted_by=OvertimeMapper._sid(lc.deleted_by),
            ),
        )