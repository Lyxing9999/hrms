from __future__ import annotations

from flask import Blueprint, request, g

from app.contexts.core.security.auth_utils import get_current_staff_id
from app.contexts.shared.decorators.response_decorator import wrap_response
from app.contexts.shared.model_converter import pydantic_converter
from app.contexts.iam.auth.jwt_utils import login_required

from app.contexts.hrms.data_transfer.request.employee_request import (
    EmployeeCreateSchema,
    EmployeeUpdateSchema,
    EmployeeCreateAccountSchema,
)
from app.contexts.hrms.data_transfer.response.employee_response import (
    EmployeeWithAccountDTO,
)
from app.contexts.hrms.mapper.employee_mapper import EmployeeMapper


employee_command_bp = Blueprint("employee_command_bp", __name__)
mapper = EmployeeMapper()


@employee_command_bp.route("/employees", methods=["POST"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def create_employee():
    """
    Create a new employee.
    """
    staff_id = get_current_staff_id()   
    payload = pydantic_converter.convert_to_model(request.json, EmployeeCreateSchema)
    employee = g.hrms.employee.create(
        payload=payload,
        created_by_user_id=staff_id,
    )

    return mapper.to_dto(employee)


@employee_command_bp.route("/employees/<employee_id>", methods=["PATCH"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def update_employee(employee_id: str):
    """
    Update an existing employee.
    """
    staff_id = get_current_staff_id()
    payload = pydantic_converter.convert_to_model(request.json, EmployeeUpdateSchema)

    employee = g.hrms.employee.update(
        employee_id=employee_id,
        payload=payload,
        actor_id=staff_id,
    )

    return mapper.to_dto(employee)


@employee_command_bp.route("/employees/<employee_id>/create-account", methods=["POST"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def create_employee_account(employee_id: str):
    """
    Create IAM account and link it to employee.
    """
    staff_id = get_current_staff_id()
    payload = pydantic_converter.convert_to_model(request.json, EmployeeCreateAccountSchema)

    iam_dto, employee = g.hrms.employee.create_account(
        employee_id=employee_id,
        payload=payload,
        created_by_user_id=staff_id,
    )

    return EmployeeWithAccountDTO(
        employee=mapper.to_dto(employee),
        user=iam_dto,
    )


@employee_command_bp.route("/employees/<employee_id>/soft-delete", methods=["DELETE"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def soft_delete_employee(employee_id: str):
    """
    Soft delete employee.
    """
    staff_id = get_current_staff_id()

    employee = g.hrms.employee.soft_delete(
        employee_id=employee_id,
        actor_id=staff_id,
    )

    return mapper.to_dto(employee)


@employee_command_bp.route("/employees/<employee_id>/restore", methods=["POST"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def restore_employee(employee_id: str):
    """
    Restore soft-deleted employee.
    """
    employee = g.hrms.employee.restore(
        employee_id=employee_id,
    )

    return mapper.to_dto(employee)