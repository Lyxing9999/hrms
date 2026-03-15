from __future__ import annotations

from bson import ObjectId
from datetime import date as date_type

from app.contexts.hrms.domain.leave import LeaveRequest
from app.contexts.shared.lifecycle.domain import Lifecycle
from app.contexts.shared.lifecycle.dto import LifecycleDTO
from app.contexts.hrms.data_transfer.response.leave_response import LeaveRequestDTO
from app.contexts.shared.model_converter import mongo_converter


class LeaveMapper:
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
        raise ValueError(f"Invalid date value: {v}")

    @staticmethod
    def to_domain(data: dict) -> LeaveRequest:
        if not isinstance(data, dict):
            raise TypeError(f"to_domain expected dict, got {type(data)}")

        lc_src = data.get("lifecycle") or {}
        lifecycle = Lifecycle(
            created_at=lc_src.get("created_at") or data.get("created_at"),
            updated_at=lc_src.get("updated_at") or data.get("updated_at"),
            deleted_at=lc_src.get("deleted_at") or data.get("deleted_at"),
            deleted_by=lc_src.get("deleted_by") or data.get("deleted_by"),
        )

        return LeaveRequest(
            id=LeaveMapper._oid(data.get("_id") or data.get("id")),
            employee_id=LeaveMapper._oid(data.get("employee_id")),
            leave_type=data.get("leave_type"),
            start_date=LeaveMapper._parse_date(data.get("start_date")),
            end_date=LeaveMapper._parse_date(data.get("end_date")),
            reason=data.get("reason") or "",
            contract_start=LeaveMapper._parse_date(data.get("contract_start")),
            contract_end=LeaveMapper._parse_date(data.get("contract_end")),
            is_paid=bool(data.get("is_paid", False)),
            status=data.get("status", "pending"),
            manager_user_id=LeaveMapper._oid(data.get("manager_user_id")),
            manager_comment=data.get("manager_comment"),
            lifecycle=lifecycle,
        )

    @staticmethod
    def to_persistence(leave_request: LeaveRequest) -> dict:
        if not isinstance(leave_request, LeaveRequest):
            raise TypeError(f"to_persistence expected LeaveRequest, got {type(leave_request)}")

        lc = leave_request.lifecycle
        doc = {
            "employee_id": LeaveMapper._oid(leave_request.employee_id),
            "leave_type": leave_request.leave_type.value if hasattr(leave_request.leave_type, "value") else str(leave_request.leave_type),
            "start_date": leave_request.start_date.isoformat(),
            "end_date": leave_request.end_date.isoformat(),
            "reason": leave_request.reason,
            "contract_start": leave_request.contract_start.isoformat(),
            "contract_end": leave_request.contract_end.isoformat(),
            "is_paid": leave_request.is_paid,
            "status": leave_request.status.value if hasattr(leave_request.status, "value") else str(leave_request.status),
            "manager_user_id": LeaveMapper._oid(leave_request.manager_user_id),
            "manager_comment": leave_request.manager_comment,
            "lifecycle": {
                "created_at": lc.created_at,
                "updated_at": lc.updated_at,
                "deleted_at": lc.deleted_at,
                "deleted_by": LeaveMapper._oid(lc.deleted_by),
            },
        }

        if leave_request.id:
            doc["_id"] = LeaveMapper._oid(leave_request.id)

        return doc

    @staticmethod
    def to_dto(leave_request: LeaveRequest) -> LeaveRequestDTO:
        lc = leave_request.lifecycle
        return LeaveRequestDTO(
            id=str(leave_request.id),
            employee_id=LeaveMapper._sid(leave_request.employee_id),
            leave_type=leave_request.leave_type.value if hasattr(leave_request.leave_type, "value") else str(leave_request.leave_type),
            start_date=leave_request.start_date,
            end_date=leave_request.end_date,
            reason=leave_request.reason,
            contract_start=leave_request.contract_start,
            contract_end=leave_request.contract_end,
            is_paid=leave_request.is_paid,
            status=leave_request.status.value if hasattr(leave_request.status, "value") else str(leave_request.status),
            manager_user_id=LeaveMapper._sid(leave_request.manager_user_id),
            manager_comment=leave_request.manager_comment,
            total_days=leave_request.total_days(),
            lifecycle=LifecycleDTO(
                created_at=lc.created_at,
                updated_at=lc.updated_at,
                deleted_at=lc.deleted_at,
                deleted_by=lc.deleted_by,
            ),
        )