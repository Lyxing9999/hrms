# app/contexts/hrms/mapper/leave_mapper.py
from bson import ObjectId
from datetime import date as date_type
from app.contexts.hrms.domain.leave import LeaveRequest
from app.contexts.shared.lifecycle.domain import Lifecycle
from app.contexts.shared.lifecycle.dto import LifecycleDTO
from app.contexts.hrms.data_transfer.response.leave_response import LeaveDTO

class LeaveMapper:
    @staticmethod
    def _oid(v):
        if v is None:
            return None
        return v if isinstance(v, ObjectId) else ObjectId(str(v))

    @staticmethod
    def to_domain(data: dict) -> LeaveRequest:
        lc_src = data.get("lifecycle") or {}
        lifecycle = Lifecycle(
            created_at=lc_src.get("created_at") or data.get("created_at"),
            updated_at=lc_src.get("updated_at") or data.get("updated_at"),
            deleted_at=lc_src.get("deleted_at") or data.get("deleted_at"),
            deleted_by=lc_src.get("deleted_by") or data.get("deleted_by"),
        )

        return LeaveRequest(
            id=LeaveMapper._oid(data.get("_id") or data.get("id")),
            employee_id=LeaveMapper._oid(data["employee_id"]),
            leave_type=data["leave_type"],
            start_date=date_type.fromisoformat(data["start_date"]),
            end_date=date_type.fromisoformat(data["end_date"]),
            reason=data.get("reason") or "",
            status=data.get("status", "pending"),
            manager_user_id=LeaveMapper._oid(data.get("manager_user_id")),
            manager_comment=data.get("manager_comment"),
            contract_start=date_type.fromisoformat(data["contract_period"]["start_date"]),
            contract_end=date_type.fromisoformat(data["contract_period"]["end_date"]),
            is_paid=bool(data.get("is_paid", False)),
            lifecycle=lifecycle,
        )

    @staticmethod
    def to_persistence(req: LeaveRequest) -> dict:
        lc = req.lifecycle
        return {
            "_id": req.id,
            "employee_id": req.employee_id,
            "leave_type": req.leave_type.value,
            "start_date": req.start_date.isoformat(),
            "end_date": req.end_date.isoformat(),
            "reason": req.reason,
            "status": req.status.value,
            "is_paid": req.is_paid,
            "manager_user_id": req.manager_user_id,
            "manager_comment": req.manager_comment,
            "contract_period": {
                "start_date": req.contract_start.isoformat(),
                "end_date": req.contract_end.isoformat(),
            },
            "lifecycle": {
                "created_at": lc.created_at,
                "updated_at": lc.updated_at,
                "deleted_at": lc.deleted_at,
                "deleted_by": lc.deleted_by,
            },
        }

    @staticmethod
    def to_dto(req: LeaveRequest) -> LeaveDTO:
        lc = req.lifecycle
        return LeaveDTO(
            id=str(req.id),
            employee_id=str(req.employee_id),
            leave_type=req.leave_type.value,
            start_date=req.start_date,
            end_date=req.end_date,
            reason=req.reason,
            contract_start=req.contract_start,
            contract_end=req.contract_end,
            is_paid=req.is_paid,
            status=req.status.value,
            manager_user_id=str(req.manager_user_id) if req.manager_user_id else None,
            manager_comment=req.manager_comment,
            lifecycle=LifecycleDTO(
                created_at=lc.created_at,
                updated_at=lc.updated_at,
                deleted_at=lc.deleted_at,
                deleted_by=lc.deleted_by,
            ),
        )