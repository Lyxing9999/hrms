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
    EmployeeAccountUpdateSchema,
    EmployeeAccountStatusSchema,
    EmployeeAssignScheduleSchema
)
from app.contexts.hrms.data_transfer.response.employee_response import (
    EmployeeWithAccountDTO,
    EmployeeAccountSummaryDTO
)
from app.contexts.hrms.mapper.employee_mapper import EmployeeMapper


employee_command_bp = Blueprint("employee_command_bp", __name__)
mapper = EmployeeMapper()


@employee_command_bp.route("/employees", methods=["POST"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def create_employee():
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
    staff_id = get_current_staff_id()
    payload = pydantic_converter.convert_to_model(request.json, EmployeeUpdateSchema)
    print("Received update payload:", payload)
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


@employee_command_bp.route("/employees/<employee_id>/account/soft-delete", methods=["POST"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def soft_delete_employee_account(employee_id: str):
    staff_id = get_current_staff_id()

    result = g.hrms.employee.soft_delete_account(
        employee_id=employee_id,
        actor_id=staff_id,
    )

    return EmployeeAccountSummaryDTO(**result)


@employee_command_bp.route("/employees/<employee_id>/account/restore", methods=["POST"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def restore_employee_account(employee_id: str):
    staff_id = get_current_staff_id()

    result = g.hrms.employee.restore_account(
        employee_id=employee_id,
        actor_id=staff_id,
    )

    return EmployeeAccountSummaryDTO(**result)


@employee_command_bp.route("/employees/<employee_id>/soft-delete", methods=["DELETE"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def soft_delete_employee(employee_id: str):
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
    employee = g.hrms.employee.restore(
        employee_id=employee_id,
    )
    return mapper.to_dto(employee)

@employee_command_bp.route("/employees/<employee_id>/link-account", methods=["POST"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def link_employee_account(employee_id: str):
    staff_id = get_current_staff_id()
    user_id = request.json.get("user_id")

    employee = g.hrms.employee.link_account(
        employee_id=employee_id,
        user_id=user_id,
        actor_id=staff_id,
    )
    return mapper.to_dto(employee)



@employee_command_bp.route("/employees/<employee_id>/account", methods=["PATCH"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def update_employee_account(employee_id: str):
    payload = pydantic_converter.convert_to_model(request.json, EmployeeAccountUpdateSchema)

    account = g.hrms.employee.update_account(
        employee_id=employee_id,
        email=payload.email,
        username=payload.username,
        password=payload.password,
    )

    return {
        "id": str(account.id),
        "email": account.email,
        "username": account.username,
        "role": account.role,
        "status": account.status,
    }


@employee_command_bp.route("/employees/<employee_id>/account/password-reset", methods=["POST"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def request_employee_account_password_reset(employee_id: str):
    staff_id = get_current_staff_id()

    result = g.hrms.employee.request_account_password_reset(
        employee_id=employee_id,
        actor_id=staff_id,
    )
    return result




@employee_command_bp.route("/employees/<user_id>/account/status", methods=["PATCH"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def set_employee_account_status(user_id: str):
    payload = pydantic_converter.convert_to_model(
        request.json,
        EmployeeAccountStatusSchema,
    )

    result = g.hrms.employee.set_account_status(
        user_id=user_id,
        status=payload.status,
    )
    return result






@employee_command_bp.route("/employees/<employee_id>/assign-schedule", methods=["POST"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def assign_employee_schedule(employee_id: str):
    staff_id = get_current_staff_id()
    payload = pydantic_converter.convert_to_model(
        request.json,
        EmployeeAssignScheduleSchema,
    )

    employee = g.hrms.employee.assign_employee_schedule(
        employee_id=employee_id,
        schedule_id=payload.schedule_id,
        actor_id=staff_id,
    )
    return mapper.to_dto(employee)