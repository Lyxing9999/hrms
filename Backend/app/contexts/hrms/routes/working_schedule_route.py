# app/contexts/hrms/routes/working_schedule_route.py
from flask import Blueprint, request, g
from app.contexts.shared.model_converter import pydantic_converter, mongo_converter
from app.contexts.shared.decorators.response_decorator import wrap_response
from app.contexts.iam.auth.jwt_utils import login_required
from app.contexts.core.security.auth_utils import get_current_staff_id
import math

from app.contexts.hrms.data_transfer.request.working_schedule_request import (
    WorkingScheduleCreateSchema,
    WorkingScheduleUpdateSchema,
)
from app.contexts.hrms.data_transfer.response.working_schedule_response import (
    WorkingScheduleDTO,
    WorkingSchedulePaginatedDTO,
)

working_schedule_bp = Blueprint("working_schedule_bp", __name__)


# -------------------------
# LIST SCHEDULES
# -------------------------
@working_schedule_bp.route("/working-schedules", methods=["GET"])
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def list_schedules():
    q = (request.args.get("q") or "").strip()
    page = max(int(request.args.get("page") or 1), 1)
    page_size = min(max(int(request.args.get("limit") or 10), 1), 100)
    
    include_deleted = (request.args.get("include_deleted") or "false").lower() == "true"
    deleted_only = (request.args.get("deleted_only") or "false").lower() == "true"
    show_deleted = "all" if include_deleted else ("deleted_only" if deleted_only else "active")
    
    items, total = g.hrms.working_schedule_service.list_schedules(
        q=q,
        page=page,
        page_size=page_size,
        show_deleted=show_deleted,
    )
    
    items_dto = [mongo_converter.doc_to_dto(g.hrms.working_schedule_service._mapper.to_persistence(item), WorkingScheduleDTO) for item in items]
    total_pages = max(1, math.ceil(int(total) / page_size))
    
    return WorkingSchedulePaginatedDTO(
        items=items_dto,
        total=int(total),
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


# -------------------------
# GET SINGLE SCHEDULE
# -------------------------
@working_schedule_bp.route("/working-schedules/<schedule_id>", methods=["GET"])
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def get_schedule(schedule_id: str):
    schedule = g.hrms.working_schedule_service.get_schedule(schedule_id)
    return mongo_converter.doc_to_dto(g.hrms.working_schedule_service._mapper.to_persistence(schedule), WorkingScheduleDTO)


# -------------------------
# GET DEFAULT SCHEDULE
# -------------------------
@working_schedule_bp.route("/working-schedules/default", methods=["GET"])
@login_required(allowed_roles=["hr_admin", "manager", "employee"])
@wrap_response
def get_default_schedule():
    schedule = g.hrms.working_schedule_service.get_default_schedule()
    if not schedule:
        return {"message": "No default schedule found"}, 404
    
    return mongo_converter.doc_to_dto(g.hrms.working_schedule_service._mapper.to_persistence(schedule), WorkingScheduleDTO)


# -------------------------
# CREATE SCHEDULE
# -------------------------
@working_schedule_bp.route("/working-schedules", methods=["POST"])
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def create_schedule():
    staff_id = get_current_staff_id()
    
    payload = pydantic_converter.convert_to_model(request.json, WorkingScheduleCreateSchema)
    schedule = g.hrms.working_schedule_service.create_schedule(payload, created_by_user_id=staff_id)
    return mongo_converter.doc_to_dto(g.hrms.working_schedule_service._mapper.to_persistence(schedule), WorkingScheduleDTO)


# -------------------------
# UPDATE SCHEDULE
# -------------------------
@working_schedule_bp.route("/working-schedules/<schedule_id>", methods=["PATCH"])
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def update_schedule(schedule_id: str):
    staff_id = get_current_staff_id()
    
    payload = pydantic_converter.convert_to_model(request.json, WorkingScheduleUpdateSchema)
    schedule = g.hrms.working_schedule_service.update_schedule(schedule_id, payload, actor_id=staff_id)
    return mongo_converter.doc_to_dto(g.hrms.working_schedule_service._mapper.to_persistence(schedule), WorkingScheduleDTO)


# -------------------------
# SOFT DELETE SCHEDULE
# -------------------------
@working_schedule_bp.route("/working-schedules/<schedule_id>/soft-delete", methods=["DELETE"])
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def soft_delete_schedule(schedule_id: str):
    staff_id = get_current_staff_id()
    
    schedule = g.hrms.working_schedule_service.soft_delete_schedule(schedule_id, actor_id=staff_id)
    return mongo_converter.doc_to_dto(g.hrms.working_schedule_service._mapper.to_persistence(schedule), WorkingScheduleDTO)


# -------------------------
# RESTORE SCHEDULE
# -------------------------
@working_schedule_bp.route("/working-schedules/<schedule_id>/restore", methods=["POST"])
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def restore_schedule(schedule_id: str):
    schedule = g.hrms.working_schedule_service.restore_schedule(schedule_id)
    return mongo_converter.doc_to_dto(g.hrms.working_schedule_service._mapper.to_persistence(schedule), WorkingScheduleDTO)
