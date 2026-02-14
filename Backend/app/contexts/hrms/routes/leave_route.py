from flask import Blueprint, request, g
from app.contexts.shared.model_converter import pydantic_converter, mongo_converter
from app.contexts.shared.decorators.response_decorator import wrap_response
from app.contexts.iam.auth.jwt_utils import login_required
from app.contexts.core.security.auth_utils import get_current_user, get_current_staff_id
import math

from app.contexts.hrms.data_transfer.request.leave_request import LeaveCreateSchema, LeaveReviewSchema, LeaveUpdateSchema
from app.contexts.hrms.data_transfer.response.leave_response import LeaveDTO, LeavePaginatedDTO

leave_bp = Blueprint("leave_bp", __name__)


# -------------------------
# LIST LEAVES (with filters)
# -------------------------
@leave_bp.route("/leaves", methods=["GET"])
@login_required(allowed_roles=["hr_admin", "manager"])
@wrap_response
def list_leaves():
    q = (request.args.get("q") or "").strip()
    page = max(int(request.args.get("page") or 1), 1)
    page_size = min(max(int(request.args.get("limit") or 10), 1), 100)
    
    employee_id = request.args.get("employee_id")
    status = request.args.get("status")
    
    include_deleted = (request.args.get("include_deleted") or "false").lower() == "true"
    deleted_only = (request.args.get("deleted_only") or "false").lower() == "true"
    show_deleted = "all" if include_deleted else ("deleted_only" if deleted_only else "active")
    
    items, total = g.hrms.leave_service.list_leaves(
        q=q,
        page=page,
        page_size=page_size,
        employee_id=employee_id,
        status=status,
        show_deleted=show_deleted,
    )
    
    items_dto = [mongo_converter.doc_to_dto(g.hrms.leave_service._mapper.to_persistence(item), LeaveDTO) for item in items]
    total_pages = max(1, math.ceil(int(total) / page_size))
    
    return LeavePaginatedDTO(
        items=items_dto,
        total=int(total),
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


# -------------------------
# GET SINGLE LEAVE
# -------------------------
@leave_bp.route("/leaves/<leave_id>", methods=["GET"])
@login_required(allowed_roles=["hr_admin", "manager", "employee"])
@wrap_response
def get_leave(leave_id: str):
    leave = g.hrms.leave_service.get_leave(leave_id)
    return mongo_converter.doc_to_dto(g.hrms.leave_service._mapper.to_persistence(leave), LeaveDTO)


# -------------------------
# EMPLOYEE SUBMIT LEAVE
# -------------------------
@leave_bp.route("/employee/leaves", methods=["POST"])
@login_required(allowed_roles=["employee", "manager"])
@wrap_response
def submit_leave():
    current = get_current_user()

    payload = pydantic_converter.convert_to_model(request.json, LeaveCreateSchema)

    # Get employee_id from current user (assuming it's stored in token or lookup)
    employee_id = payload.employee_id or current.get("employee_id")
    if not employee_id:
        raise ValueError("Employee ID is required")
    
    leave = g.hrms.leave_service.submit_contract_leave(employee_id, payload)
    return leave


# -------------------------
# UPDATE LEAVE (before review)
# -------------------------
@leave_bp.route("/leaves/<leave_id>", methods=["PATCH"])
@login_required(allowed_roles=["hr_admin", "employee"])
@wrap_response
def update_leave(leave_id: str):
    staff_id = get_current_staff_id()
    
    payload = pydantic_converter.convert_to_model(request.json, LeaveUpdateSchema)
    leave = g.hrms.leave_service.update_leave(leave_id, payload, actor_id=staff_id)
    return mongo_converter.doc_to_dto(g.hrms.leave_service._mapper.to_persistence(leave), LeaveDTO)


# -------------------------
# MANAGER APPROVE
# -------------------------
@leave_bp.route("/manager/leaves/<leave_id>/approve", methods=["PATCH"])
@login_required(allowed_roles=["manager", "hr_admin"])
@wrap_response
def approve_leave(leave_id: str):
    current = get_current_user()

    payload = pydantic_converter.convert_to_model(request.json or {}, LeaveReviewSchema)
    return g.hrms.leave_service.approve_leave(leave_id, current["user_id"], payload.comment)


# -------------------------
# MANAGER REJECT
# -------------------------
@leave_bp.route("/manager/leaves/<leave_id>/reject", methods=["PATCH"])
@login_required(allowed_roles=["manager", "hr_admin"])
@wrap_response
def reject_leave(leave_id: str):
    current = get_current_user()

    payload = pydantic_converter.convert_to_model(request.json or {}, LeaveReviewSchema)
    return g.hrms.leave_service.reject_leave(leave_id, current["user_id"], payload.comment)


# -------------------------
# CANCEL LEAVE (by employee)
# -------------------------
@leave_bp.route("/leaves/<leave_id>/cancel", methods=["PATCH"])
@login_required(allowed_roles=["employee", "hr_admin"])
@wrap_response
def cancel_leave(leave_id: str):
    staff_id = get_current_staff_id()
    
    leave = g.hrms.leave_service.cancel_leave(leave_id, actor_id=staff_id)
    return mongo_converter.doc_to_dto(g.hrms.leave_service._mapper.to_persistence(leave), LeaveDTO)


# -------------------------
# SOFT DELETE LEAVE
# -------------------------
@leave_bp.route("/leaves/<leave_id>/soft-delete", methods=["DELETE"])
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def soft_delete_leave(leave_id: str):
    staff_id = get_current_staff_id()
    
    leave = g.hrms.leave_service.soft_delete_leave(leave_id, actor_id=staff_id)
    return mongo_converter.doc_to_dto(g.hrms.leave_service._mapper.to_persistence(leave), LeaveDTO)


# -------------------------
# RESTORE LEAVE
# -------------------------
@leave_bp.route("/leaves/<leave_id>/restore", methods=["POST"])
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def restore_leave(leave_id: str):
    leave = g.hrms.leave_service.restore_leave(leave_id)
    return mongo_converter.doc_to_dto(g.hrms.leave_service._mapper.to_persistence(leave), LeaveDTO)