from __future__ import annotations

from flask import Blueprint, request, g

from app.contexts.shared.decorators.response_decorator import wrap_response
from app.contexts.iam.auth.jwt_utils import login_required
from app.contexts.hrms.mapper.work_location_mapper import WorkLocationMapper


work_location_query_bp = Blueprint("work_location_query_bp", __name__)
mapper = WorkLocationMapper()


@work_location_query_bp.route("/work-locations", methods=["GET"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin", "employee", "manager", "payroll_manager"])
@wrap_response
def list_work_locations():
    q = request.args.get("q", "")
    status = request.args.get("status", "all")

    items = g.hrms.work_location.list(q=q, status=status)
    return [mapper.to_dto(item).model_dump(mode="json") for item in items]


@work_location_query_bp.route("/work-locations/<location_id>", methods=["GET"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin", "employee", "manager", "payroll_manager"])
@wrap_response
def get_work_location(location_id: str):
    item = g.hrms.work_location.get(location_id=location_id)
    return mapper.to_dto(item).model_dump(mode="json")


@work_location_query_bp.route("/work-locations/active", methods=["GET"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin", "employee", "manager", "payroll_manager"])
@wrap_response
def get_active_work_location():
    item = g.hrms.work_location.get_active()
    return mapper.to_dto(item).model_dump(mode="json") if item else None