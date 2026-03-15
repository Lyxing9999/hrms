from __future__ import annotations

from bson import ObjectId
from datetime import date as date_type

from app.contexts.hrms.domain.overtime import OvertimeRequest
from app.contexts.shared.lifecycle.domain import Lifecycle
from app.contexts.shared.lifecycle.dto import LifecycleDTO
from app.contexts.hrms.data_transfer.response.overtime_response import OvertimeRequestDTO
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
    def _parse_date(v) -> date_type:
        if isinstance(v, date_type):
            return v
        if isinstance(v, str):
            return date_type.fromisoformat(v)
        raise ValueError(f"Invalid request_date: {v}")

    @staticmethod
    def to_domain(data: dict) -> OvertimeRequest:
        if not isinstance(data, dict):
            raise TypeError(f"to_domain expected dict, got {type(data)}")

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
            request_date=OvertimeMapper._parse_date(data.get("request_date")),
            start_time=data.get("start_time"),
            end_time=data.get("end_time"),
            schedule_end_time=data.get("schedule_end_time"),
            reason=data.get("reason") or "",
            day_type=data.get("day_type"),
            basic_salary=float(data.get("basic_salary", 0)),
            submitted_at=data.get("submitted_at"),
            status=data.get("status", "pending"),
            manager_id=OvertimeMapper._oid(data.get("manager_id")),
            manager_comment=data.get("manager_comment"),
            approved_hours=float(data.get("approved_hours", 0)),
            calculated_payment=float(data.get("calculated_payment", 0)),
            lifecycle=lifecycle,
        )

    @staticmethod
    def to_persistence(overtime: OvertimeRequest) -> dict:
        if not isinstance(overtime, OvertimeRequest):
            raise TypeError(f"to_persistence expected OvertimeRequest, got {type(overtime)}")

        lc = overtime.lifecycle
        doc = {
            "employee_id": OvertimeMapper._oid(overtime.employee_id),
            "request_date": overtime.request_date.isoformat(),
            "start_time": overtime.start_time,
            "end_time": overtime.end_time,
            "schedule_end_time": overtime.schedule_end_time,
            "reason": overtime.reason,
            "day_type": overtime.day_type.value if hasattr(overtime.day_type, "value") else str(overtime.day_type),
            "basic_salary": overtime.basic_salary,
            "submitted_at": overtime.submitted_at,
            "status": overtime.status.value if hasattr(overtime.status, "value") else str(overtime.status),
            "manager_id": OvertimeMapper._oid(overtime.manager_id),
            "manager_comment": overtime.manager_comment,
            "approved_hours": overtime.approved_hours,
            "calculated_payment": overtime.calculated_payment,
            "month": overtime.request_date.strftime("%Y-%m"),
            "lifecycle": {
                "created_at": lc.created_at,
                "updated_at": lc.updated_at,
                "deleted_at": lc.deleted_at,
                "deleted_by": OvertimeMapper._oid(lc.deleted_by),
            },
        }

        if overtime.id:
            doc["_id"] = OvertimeMapper._oid(overtime.id)

        return doc

    @staticmethod
    def to_dto(overtime: OvertimeRequest) -> OvertimeRequestDTO:
        lc = overtime.lifecycle
        return OvertimeRequestDTO(
            id=str(overtime.id),
            employee_id=OvertimeMapper._sid(overtime.employee_id),
            request_date=overtime.request_date,
            start_time=overtime.start_time,
            end_time=overtime.end_time,
            schedule_end_time=overtime.schedule_end_time,
            reason=overtime.reason,
            day_type=overtime.day_type.value if hasattr(overtime.day_type, "value") else str(overtime.day_type),
            basic_salary=overtime.basic_salary,
            submitted_at=overtime.submitted_at,
            status=overtime.status.value if hasattr(overtime.status, "value") else str(overtime.status),
            manager_id=OvertimeMapper._sid(overtime.manager_id),
            manager_comment=overtime.manager_comment,
            approved_hours=overtime.approved_hours,
            calculated_payment=overtime.calculated_payment,
            lifecycle=LifecycleDTO(
                created_at=lc.created_at,
                updated_at=lc.updated_at,
                deleted_at=lc.deleted_at,
                deleted_by=lc.deleted_by,
            ),
        )