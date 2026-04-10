from __future__ import annotations

from bson import ObjectId

from app.contexts.hrms.domain.leave import LeaveRequest
from app.contexts.hrms.data_transfer.response.leave_response import LeaveRequestDTO
from app.contexts.shared.lifecycle.domain import Lifecycle
from app.contexts.shared.lifecycle.dto import LifecycleDTO
from app.contexts.shared.model_converter import mongo_converter
from app.contexts.shared.time_utils import coerce_date

class LeaveMapper:
    @staticmethod
    def _oid(v) -> ObjectId | None:
        if v is None:
            return None
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str) and v.strip().lower() in {"", "null", "none", "undefined"}:
            return None
        return mongo_converter.convert_to_object_id(v)

    @staticmethod
    def _sid(v) -> str | None:
        if v is None:
            return None
        return str(v)

    @staticmethod
    def to_domain(data: dict | LeaveRequest) -> LeaveRequest:
        if isinstance(data, LeaveRequest):
            return data

        lc_src = data.get("lifecycle") or {}
        lifecycle = Lifecycle(
            created_at=lc_src.get("created_at") or data.get("created_at"),
            updated_at=lc_src.get("updated_at") or data.get("updated_at"),
            deleted_at=lc_src.get("deleted_at") or data.get("deleted_at"),
            deleted_by=lc_src.get("deleted_by") or data.get("deleted_by"),
        )

        start_date = coerce_date(data.get("start_date"))
        end_date = coerce_date(data.get("end_date"))
        contract_start = coerce_date(data.get("contract_start"))
        contract_end = coerce_date(data.get("contract_end"))

        if contract_start is None:
            contract_start = start_date
        if contract_end is None:
            contract_end = end_date

        return LeaveRequest(
            id=LeaveMapper._oid(data.get("_id") or data.get("id")),
            employee_id=LeaveMapper._oid(data.get("employee_id")),
            leave_type=data.get("leave_type"),
            start_date=start_date,
            end_date=end_date,
            reason=data.get("reason"),
            contract_start=contract_start,
            contract_end=contract_end,
            is_paid=bool(data.get("is_paid", False)),
            status=data.get("status"),
            manager_user_id=LeaveMapper._oid(data.get("manager_user_id")),
            manager_comment=data.get("manager_comment"),
            lifecycle=lifecycle,
        )

    @staticmethod
    def to_persistence(leave: LeaveRequest) -> dict:
        lc = leave.lifecycle
        doc = {
            "employee_id": LeaveMapper._oid(leave.employee_id),
            "leave_type": leave.leave_type.value if hasattr(leave.leave_type, "value") else str(leave.leave_type),
            "start_date": leave.start_date.isoformat() if leave.start_date else None,
            "end_date": leave.end_date.isoformat() if leave.end_date else None,
            "reason": leave.reason,
            "contract_start": leave.contract_start.isoformat() if leave.contract_start else None,
            "contract_end": leave.contract_end.isoformat() if leave.contract_end else None,
            "is_paid": leave.is_paid,
            "status": leave.status.value if hasattr(leave.status, "value") else str(leave.status),
            "manager_user_id": LeaveMapper._oid(leave.manager_user_id),
            "manager_comment": leave.manager_comment,
            "lifecycle": {
                "created_at": lc.created_at,
                "updated_at": lc.updated_at,
                "deleted_at": lc.deleted_at,
                "deleted_by": LeaveMapper._oid(lc.deleted_by),
            },
        }

        if leave.id:
            doc["_id"] = LeaveMapper._oid(leave.id)

        return doc

    @staticmethod
    def to_dto(data: LeaveRequest | dict) -> LeaveRequestDTO:
        leave = LeaveMapper.to_domain(data)
        lc = leave.lifecycle

        return LeaveRequestDTO(
            id=str(leave.id),
            employee_id=LeaveMapper._sid(leave.employee_id),
            leave_type=leave.leave_type.value if hasattr(leave.leave_type, "value") else str(leave.leave_type),
            start_date=leave.start_date,
            end_date=leave.end_date,
            reason=leave.reason,
            contract_start=leave.contract_start,
            contract_end=leave.contract_end,
            is_paid=leave.is_paid,
            status=leave.status.value if hasattr(leave.status, "value") else str(leave.status),
            manager_user_id=LeaveMapper._sid(leave.manager_user_id),
            manager_comment=leave.manager_comment,
            total_days=leave.total_days(),
            lifecycle=LifecycleDTO(
                created_at=lc.created_at,
                updated_at=lc.updated_at,
                deleted_at=lc.deleted_at,
                deleted_by=LeaveMapper._sid(lc.deleted_by),
            ),
        )