from __future__ import annotations

from flask import Blueprint, request, g

from app.contexts.core.security.auth_utils import get_current_user_oid
from app.contexts.shared.decorators.response_decorator import wrap_response
from app.contexts.shared.model_converter import pydantic_converter
from app.contexts.iam.auth.jwt_utils import login_required

from app.contexts.hrms.data_transfer.request.payroll_request import GeneratePayrollSchema
from app.contexts.hrms.mapper.payroll_mapper import PayrollMapper


payroll_command_bp = Blueprint("payroll_command_bp", __name__)
mapper = PayrollMapper()


@payroll_command_bp.route("/payroll/runs/generate", methods=["POST"], strict_slashes=False)
@login_required(allowed_roles=["payroll_manager", "hr_admin"])
@wrap_response
def generate_monthly_payroll():
    actor_id = get_current_user_oid()
    payload = pydantic_converter.convert_to_model(request.json, GeneratePayrollSchema)

    result = g.hrms.payroll.generate_monthly(
        month=payload.month,
        generated_by=actor_id,
    )

    return {
        "payroll_run": mapper.payroll_run_to_dto(result["payroll_run"]).model_dump(mode="json"),
        "payslips": [mapper.payslip_to_dto(x).model_dump(mode="json") for x in result["payslips"]],
    }


@payroll_command_bp.route("/payroll/runs/<payroll_run_id>/finalize", methods=["POST"], strict_slashes=False)
@login_required(allowed_roles=["payroll_manager", "hr_admin"])
@wrap_response
def finalize_payroll_run(payroll_run_id: str):
    actor_id = get_current_user_oid()
    run = g.hrms.payroll.finalize(payroll_run_id=payroll_run_id, actor_id=actor_id)
    return mapper.payroll_run_to_dto(run).model_dump(mode="json")


@payroll_command_bp.route("/payroll/runs/<payroll_run_id>/mark-paid", methods=["POST"], strict_slashes=False)
@login_required(allowed_roles=["payroll_manager", "hr_admin"])
@wrap_response
def mark_payroll_run_paid(payroll_run_id: str):
    actor_id = get_current_user_oid()
    run = g.hrms.payroll.mark_paid(payroll_run_id=payroll_run_id, actor_id=actor_id)
    return mapper.payroll_run_to_dto(run).model_dump(mode="json")