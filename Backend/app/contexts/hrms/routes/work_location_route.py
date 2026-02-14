# app/contexts/hrms/routes/work_location_route.py
from flask import Blueprint, request, g
from app.contexts.shared.model_converter import pydantic_converter, mongo_converter
from app.contexts.shared.decorators.response_decorator import wrap_response
from app.contexts.iam.auth.jwt_utils import login_required
from app.contexts.core.security.auth_utils import get_current_staff_id
import math

from app.contexts.hrms.data_transfer.request.work_location_request import (
    WorkLocationCreateSchema,
    WorkLocationUpdateSchema,
)
from app.contexts.hrms.data_transfer.response.work_location_response import (
    WorkLocationDTO,
    WorkLocationPaginatedDTO,
)

work_location_bp = Blueprint("work_location_bp", __name__)


# -------------------------
# LIST LOCATIONS
# -------------------------
@work_location_bp.route("/work-locations", methods=["GET"])
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def list_locations():
    q = (request.args.get("q") or "").strip()
    page = max(int(request.args.get("page") or 1), 1)
    page_size = min(max(int(request.args.get("limit") or 10), 1), 100)
    
    is_active_str = request.args.get("is_active")
    is_active = None if is_active_str is None else is_active_str.lower() == "true"
    
    include_deleted = (request.args.get("include_deleted") or "false").lower() == "true"
    deleted_only = (request.args.get("deleted_only") or "false").lower() == "true"
    show_deleted = "all" if include_deleted else ("deleted_only" if deleted_only else "active")
    
    items, total = g.hrms.work_location_service.list_locations(
        q=q,
        page=page,
        page_size=page_size,
        is_active=is_active,
        show_deleted=show_deleted,
    )
    
    items_dto = [mongo_converter.doc_to_dto(g.hrms.work_location_service._mapper.to_persistence(item), WorkLocationDTO) for item in items]
    total_pages = max(1, math.ceil(int(total) / page_size))
    
    return WorkLocationPaginatedDTO(
        items=items_dto,
        total=int(total),
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


# -------------------------
# GET ACTIVE LOCATIONS (for check-in)
# -------------------------
@work_location_bp.route("/work-locations/active", methods=["GET"])
@login_required(allowed_roles=["hr_admin", "manager", "employee"])
@wrap_response
def get_active_locations():
    locations = g.hrms.work_location_service.get_active_locations()
    items_dto = [mongo_converter.doc_to_dto(g.hrms.work_location_service._mapper.to_persistence(loc), WorkLocationDTO) for loc in locations]
    
    return {"items": items_dto}


# -------------------------
# GET SINGLE LOCATION
# -------------------------
@work_location_bp.route("/work-locations/<location_id>", methods=["GET"])
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def get_location(location_id: str):
    location = g.hrms.work_location_service.get_location(location_id)
    return mongo_converter.doc_to_dto(g.hrms.work_location_service._mapper.to_persistence(location), WorkLocationDTO)


# -------------------------
# CREATE LOCATION
# -------------------------
@work_location_bp.route("/work-locations", methods=["POST"])
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def create_location():
    staff_id = get_current_staff_id()
    
    payload = pydantic_converter.convert_to_model(request.json, WorkLocationCreateSchema)
    location = g.hrms.work_location_service.create_location(payload, created_by_user_id=staff_id)
    return mongo_converter.doc_to_dto(g.hrms.work_location_service._mapper.to_persistence(location), WorkLocationDTO)


# -------------------------
# UPDATE LOCATION
# -------------------------
@work_location_bp.route("/work-locations/<location_id>", methods=["PATCH"])
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def update_location(location_id: str):
    staff_id = get_current_staff_id()
    
    payload = pydantic_converter.convert_to_model(request.json, WorkLocationUpdateSchema)
    location = g.hrms.work_location_service.update_location(location_id, payload, actor_id=staff_id)
    return mongo_converter.doc_to_dto(g.hrms.work_location_service._mapper.to_persistence(location), WorkLocationDTO)


# -------------------------
# SOFT DELETE LOCATION
# -------------------------
@work_location_bp.route("/work-locations/<location_id>/soft-delete", methods=["DELETE"])
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def soft_delete_location(location_id: str):
    staff_id = get_current_staff_id()
    
    location = g.hrms.work_location_service.soft_delete_location(location_id, actor_id=staff_id)
    return mongo_converter.doc_to_dto(g.hrms.work_location_service._mapper.to_persistence(location), WorkLocationDTO)


# -------------------------
# RESTORE LOCATION
# -------------------------
@work_location_bp.route("/work-locations/<location_id>/restore", methods=["POST"])
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def restore_location(location_id: str):
    location = g.hrms.work_location_service.restore_location(location_id)
    return mongo_converter.doc_to_dto(g.hrms.work_location_service._mapper.to_persistence(location), WorkLocationDTO)
