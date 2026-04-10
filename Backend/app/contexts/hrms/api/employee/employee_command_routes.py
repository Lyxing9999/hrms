from __future__ import annotations

from flask import Blueprint, request, g

from app.contexts.core.security.auth_utils import get_current_user_id
from app.contexts.shared.decorators.response_decorator import wrap_response
from app.contexts.shared.model_converter import pydantic_converter
from app.contexts.iam.auth.jwt_utils import login_required
from app.contexts.iam.mapper.iam_mapper import IAMMapper

from app.contexts.hrms.data_transfer.request.employee_request import (
    EmployeeCreateSchema,
    EmployeeOnboardSchema,
    EmployeeUpdateSchema,
    EmployeeCreateAccountSchema,
    EmployeeAccountUpdateSchema,
    EmployeeAccountStatusSchema,
    EmployeeAssignScheduleSchema,
)
from app.contexts.hrms.data_transfer.response.employee_response import (
    EmployeeWithAccountDTO,
    EmployeeAccountSummaryDTO,
)
from app.contexts.hrms.mapper.employee_mapper import EmployeeMapper
from app.contexts.hrms.integrations.iam_gateway import HRMSIamGateway


# we will refector zoon add actor_id to all use cases,

employee_command_bp = Blueprint("employee_command_bp", __name__)
mapper = EmployeeMapper()


@employee_command_bp.route("/employees", methods=["POST"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def create_employee():
    actor_user_id = get_current_user_id()
    payload = pydantic_converter.convert_to_model(request.json, EmployeeCreateSchema)

    employee = g.hrms.employee.create(
        payload=payload,
        created_by_user_id=actor_user_id,
    )
    return mapper.to_dto(employee)


@employee_command_bp.route("/employees/<employee_id>", methods=["PATCH"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def update_employee(employee_id: str):
    actor_user_id = get_current_user_id()
    payload = pydantic_converter.convert_to_model(request.json, EmployeeUpdateSchema)

    employee = g.hrms.employee.update(
        employee_id=employee_id,
        payload=payload,
        actor_id=actor_user_id,
    )
    return mapper.to_dto(employee)


@employee_command_bp.route("/employees/<employee_id>/create-account", methods=["POST"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def create_employee_account(employee_id: str):
    actor_user_id = get_current_user_id()
    payload = pydantic_converter.convert_to_model(request.json, EmployeeCreateAccountSchema)

    iam_gateway = HRMSIamGateway(db=g.db)

    iam_user, employee = g.hrms.employee.create_account(
        employee_id=employee_id,
        payload=payload,
        created_by_user_id=actor_user_id,
    )

    return EmployeeWithAccountDTO(
        employee=mapper.to_dto(employee),
        user=iam_gateway.to_account_dto(iam_user),
    )


@employee_command_bp.route("/employees/<employee_id>/account/soft-delete", methods=["POST"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def soft_delete_employee_account(employee_id: str):
    actor_user_id = get_current_user_id()

    result = g.hrms.employee.soft_delete_account(
        employee_id=employee_id,
        actor_id=actor_user_id,
    )
    return EmployeeAccountSummaryDTO(**result)


@employee_command_bp.route("/employees/<employee_id>/account/restore", methods=["POST"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def restore_employee_account(employee_id: str):
    actor_user_id = get_current_user_id()

    result = g.hrms.employee.restore_account(
        employee_id=employee_id,
        actor_id=actor_user_id,
    )
    return EmployeeAccountSummaryDTO(**result)


@employee_command_bp.route("/employees/<employee_id>/soft-delete", methods=["DELETE"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def soft_delete_employee(employee_id: str):
    actor_user_id = get_current_user_id()

    employee = g.hrms.employee.soft_delete(
        employee_id=employee_id,
        actor_id=actor_user_id,
    )
    return mapper.to_dto(employee)




@employee_command_bp.route("/employees/<employee_id>/link-account", methods=["POST"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def link_employee_account(employee_id: str):
    actor_user_id = get_current_user_id()
    body = request.json or {}
    user_id = body.get("user_id")

    if not user_id:
        raise ValueError("user_id is required")

    employee = g.hrms.employee.link_account(
        employee_id=employee_id,
        user_id=user_id,
    )
    return mapper.to_dto(employee)


@employee_command_bp.route("/employees/<employee_id>/account", methods=["PATCH"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def update_employee_account(employee_id: str):
    actor_user_id = get_current_user_id()
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
    actor_user_id = get_current_user_id()

    result = g.hrms.employee.request_account_password_reset(
        employee_id=employee_id,
    )
    return result


@employee_command_bp.route("/employees/<employee_id>/account/reset-password", methods=["POST"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def reset_employee_account_password(employee_id: str):
    actor_user_id = get_current_user_id()
    body = request.json or {}
    new_password = str(body.get("new_password") or "").strip()

    if not new_password:
        raise ValueError("new_password is required")

    result = g.hrms.employee.change_account_password(
        employee_id=employee_id,
        new_password=new_password,
    )
    return result


# Better route name than /employees/<user_id>/account/status would be:
# /employee-accounts/<user_id>/status
# But if you keep current route, this version is still consistent internally.
@employee_command_bp.route("/employees/<user_id>/account/status", methods=["PATCH"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def set_employee_account_status(user_id: str):
    actor_user_id = get_current_user_id()
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
    actor_user_id = get_current_user_id()
    payload = pydantic_converter.convert_to_model(
        request.json,
        EmployeeAssignScheduleSchema,
    )

    employee = g.hrms.employee.assign_employee_schedule(
        employee_id=employee_id,
        schedule_id=payload.schedule_id,
        actor_id = actor_user_id,
    )
    return mapper.to_dto(employee)


@employee_command_bp.route("/employees/onboard", methods=["POST"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def onboard_employee_with_account():
    actor_user_id = get_current_user_id()
    payload = pydantic_converter.convert_to_model(request.json, EmployeeOnboardSchema)

    iam_user, employee = g.hrms.employee.onboard_with_account(
        employee_payload=payload.employee,
        email=payload.email,
        password=payload.password,
        username=payload.username,
        role=payload.role,
        created_by_user_id=actor_user_id,
    )

    return EmployeeWithAccountDTO(
        employee=mapper.to_dto(employee),
        user=IAMMapper.to_dto(iam_user),
    )



@employee_command_bp.route("/employees/<employee_id>/restore", methods=["POST"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def restore_employee(employee_id: str):
    actor_user_id = get_current_user_id()

    employee = g.hrms.employee.restore(
        employee_id=employee_id,
    )
    return mapper.to_dto(employee)