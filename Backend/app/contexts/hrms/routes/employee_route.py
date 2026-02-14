from app.contexts.core.security.auth_utils import get_current_staff_id
from flask import Blueprint, request, g
import math

from app.contexts.shared.decorators.response_decorator import wrap_response
from app.contexts.shared.model_converter import pydantic_converter, mongo_converter
from app.contexts.iam.auth.jwt_utils import login_required

from app.contexts.hrms.data_transfer.request.employee_request import (
    EmployeeCreateSchema,
    EmployeeCreateAccountSchema,
)
from app.contexts.hrms.data_transfer.response.employee_response import (
    EmployeeDTO,
    EmployeePaginatedDTO,
    EmployeeWithAccountDTO,
)


employee_bp = Blueprint("employee_bp", __name__)


@employee_bp.route("/employees", methods=["GET"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def list_employees():
    q = (request.args.get("q") or "").strip()
    page = max(int(request.args.get("page") or 1), 1)
    page_size = min(max(int(request.args.get("limit") or 10), 1), 100)

    include_deleted = (request.args.get("include_deleted") or "false").lower() == "true"
    deleted_only = (request.args.get("deleted_only") or "false").lower() == "true"
    show_deleted = "all" if include_deleted else ("deleted_only" if deleted_only else "active")

    item , total = g.hrms.employee_service.list_employees(
        q=q,
        page=page,
        page_size=page_size,
        show_deleted=show_deleted,
    )

    items_dto = mongo_converter.list_to_dto(item, EmployeeDTO)
    total_pages = max(1, math.ceil(int(total) / page_size))

    return EmployeePaginatedDTO(
        items=items_dto,
        total=int(total),
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@employee_bp.route("/employees/<employee_id>", methods=["GET"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def get_employee(employee_id: str):
    emp = g.hrms.employee_service.get_employee(employee_id)  
    return mongo_converter.doc_to_dto(emp, EmployeeDTO)


@employee_bp.route("/employees", methods=["POST"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def create_employee():
    staff_id = get_current_staff_id()

    payload = pydantic_converter.convert_to_model(request.json, EmployeeCreateSchema)
    emp = g.hrms.employee_service.create_employee(payload, created_by_user_id=staff_id)  # domain
    return mongo_converter.doc_to_dto(g.hrms.employee_service._mapper.to_persistence(emp), EmployeeDTO)


@employee_bp.route("/employees/<employee_id>/create-account", methods=["POST"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def create_employee_account(employee_id: str):
    staff_id = get_current_staff_id()

    payload = pydantic_converter.convert_to_model(request.json, EmployeeCreateAccountSchema)
    iam_dto, emp = g.hrms.employee_service.create_account_for_employee(employee_id, payload, created_by_user_id=staff_id)

    employee_dto = mongo_converter.doc_to_dto(emp, EmployeeDTO)
    return EmployeeWithAccountDTO(employee=employee_dto, user=iam_dto)


@employee_bp.route("/employees/<employee_id>", methods=["PATCH"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def update_employee(employee_id: str):
    staff_id = get_current_staff_id()

    from app.contexts.hrms.data_transfer.request.employee_request import EmployeeUpdateSchema
    payload = pydantic_converter.convert_to_model(request.json, EmployeeUpdateSchema)
    emp = g.hrms.employee_service.update_employee(employee_id, payload, actor_id=staff_id)
    return mongo_converter.doc_to_dto(g.hrms.employee_service._mapper.to_persistence(emp), EmployeeDTO)

@employee_bp.route("/employees/my-attendace", methods=["GET"], strict_slashes=False)
@login_required(allowed_roles=["employee"])
def get_my_id():
    staff_id = get_current_staff_id()
    attendance_emnployee = g.hrms.employee_service.get_my_attendance(staff_id)
    return mongo_converter.doc_to_dto(g.hrms.employee_service.mapper(emp), EmployeeDTO)

@employee_bp.route("/employees/<employee_id>/soft-delete", methods=["DELETE"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def soft_delete_employee(employee_id: str):
    staff_id = get_current_staff_id()

    emp = g.hrms.employee_service.soft_delete_employee(employee_id, actor_id=staff_id)  # domain
    return mongo_converter.doc_to_dto(emp, EmployeeDTO)


@employee_bp.route("/employees/<employee_id>/restore", methods=["POST"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def restore_employee(employee_id: str):
    emp = g.hrms.employee_service.restore_employee(employee_id)
    return mongo_converter.doc_to_dto(g.hrms.employee_service._mapper.to_persistence(emp), EmployeeDTO)