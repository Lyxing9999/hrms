from __future__ import annotations

import math

from flask import Blueprint, request, g

from app.contexts.core.security.auth_utils import get_current_user_id
from app.contexts.shared.decorators.response_decorator import wrap_response
from app.contexts.iam.auth.jwt_utils import login_required

from app.contexts.hrms.mapper.employee_mapper import EmployeeMapper
from app.contexts.hrms.data_transfer.response.employee_response import (
    EmployeePaginatedDTO,
)


employee_query_bp = Blueprint("employee_query_bp", __name__)
mapper = EmployeeMapper()


@employee_query_bp.route("/employees", methods=["GET"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def list_employees():
    """
    List employees with pagination and deleted filters.
    """
    q = (request.args.get("q") or "").strip()
    page = max(int(request.args.get("page") or 1), 1)
    page_size = min(max(int(request.args.get("limit") or 10), 1), 100)

    include_deleted = (request.args.get("include_deleted") or "false").lower() == "true"
    deleted_only = (request.args.get("deleted_only") or "false").lower() == "true"
    show_deleted = "all" if include_deleted else ("deleted_only" if deleted_only else "active")

    items, total = g.hrms.employee.list(
        q=q,
        page=page,
        page_size=page_size,
        show_deleted=show_deleted,
    )

    total_pages = max(1, math.ceil(int(total) / page_size))

    return EmployeePaginatedDTO(
        items=[mapper.to_dto(item) for item in items],
        total=int(total),
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@employee_query_bp.route("/employees/<employee_id>", methods=["GET"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def get_employee(employee_id: str):
    """
    Get employee detail by id.
    """
    employee = g.hrms.employee.get(
        employee_id=employee_id,
    )

    return mapper.to_dto(employee)


@employee_query_bp.route("/employees/me", methods=["GET"], strict_slashes=False)
@login_required(allowed_roles=["employee", "manager", "payroll_manager", "hr_admin"])
@wrap_response
def get_my_employee_profile():
    """
    Get current logged-in user's employee profile.
    """
    user_id = get_current_user_id()

    employee = g.hrms.employee.me(
        user_id=user_id,
    )

    return mapper.to_dto(employee)