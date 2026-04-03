from __future__ import annotations

from flask import Blueprint, request, g

from app.contexts.core.security.auth_utils import get_current_staff_id
from app.contexts.shared.decorators.response_decorator import wrap_response
from app.contexts.iam.auth.jwt_utils import login_required
from app.contexts.hrms.mapper.overtime_mapper import OvertimeMapper


overtime_query_bp = Blueprint("overtime_query_bp", __name__)
mapper = OvertimeMapper()


@overtime_query_bp.route("/overtime-requests", methods=["GET"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin", "manager"])
@wrap_response
def list_overtime_requests():
    employee_id = request.args.get("employee_id")
    status = request.args.get("status")
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))

    items, total = g.hrms.overtime.list(
        employee_id=employee_id,
        status=status,
        page=page,
        limit=limit,
    )

    return {
        "items": [mapper.to_dto(item).model_dump(mode="json") for item in items],
        "total": total,
        "page": page,
        "limit": limit,
    }


@overtime_query_bp.route("/overtime-requests/my", methods=["GET"], strict_slashes=False)
@login_required(allowed_roles=["employee"])
@wrap_response
def list_my_overtime_requests():
    user_id = get_current_staff_id()
    status = request.args.get("status")
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))

    items, total = g.hrms.overtime.list_my(
        user_id=user_id,
        status=status,
        page=page,
        limit=limit,
    )

    return {
        "items": [mapper.to_dto(item).model_dump(mode="json") for item in items],
        "total": total,
        "page": page,
        "limit": limit,
    }


@overtime_query_bp.route("/overtime-requests/<overtime_id>", methods=["GET"], strict_slashes=False)
@login_required(allowed_roles=["employee", "manager", "hr_admin", "payroll_manager"])
@wrap_response
def get_overtime_request(overtime_id: str):
    overtime = g.hrms.overtime.get(overtime_id=overtime_id)
    return mapper.to_dto(overtime).model_dump(mode="json")


@overtime_query_bp.route("/overtime-requests/payroll-approved", methods=["GET"], strict_slashes=False)
@login_required(allowed_roles=["payroll_manager", "hr_admin"])
@wrap_response
def list_approved_overtime_for_payroll():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    items = g.hrms.overtime.list_approved_for_payroll(
        start_date=start_date,
        end_date=end_date,
    )

    return [mapper.to_dto(item).model_dump(mode="json") for item in items]