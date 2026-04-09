from __future__ import annotations

from flask import Blueprint, request, g

from app.contexts.core.security.auth_utils import get_current_user_id
from app.contexts.shared.decorators.response_decorator import wrap_response
from app.contexts.shared.model_converter import pydantic_converter
from app.contexts.iam.auth.jwt_utils import login_required

from app.contexts.hrms.data_transfer.request.deduction_rule_request import (
    DeductionRuleCreateSchema,
    DeductionRuleUpdateSchema,
)
from app.contexts.hrms.mapper.deduction_rule_mapper import DeductionRuleMapper


deduction_rule_command_bp = Blueprint("deduction_rule_command_bp", __name__)
mapper = DeductionRuleMapper()


@deduction_rule_command_bp.route("/deduction-rules", methods=["POST"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def create_deduction_rule():
    staff_id = get_current_user_id()
    payload = pydantic_converter.convert_to_model(request.json, DeductionRuleCreateSchema)

    rule = g.hrms.deduction_rule.create(
        payload=payload,
        created_by_user_id=staff_id,
    )
    return mapper.to_dto(rule)


@deduction_rule_command_bp.route("/deduction-rules/<rule_id>", methods=["PATCH"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def update_deduction_rule(rule_id: str):
    payload = pydantic_converter.convert_to_model(request.json, DeductionRuleUpdateSchema)
    rule = g.hrms.deduction_rule.update(
        rule_id=rule_id,
        payload=payload,
    )
    return mapper.to_dto(rule)


@deduction_rule_command_bp.route("/deduction-rules/<rule_id>", methods=["DELETE"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def soft_delete_deduction_rule(rule_id: str):
    actor_id = get_current_user_id()
    rule = g.hrms.deduction_rule.soft_delete(
        rule_id=rule_id,
        actor_id=actor_id,
    )
    return mapper.to_dto(rule)


@deduction_rule_command_bp.route("/deduction-rules/<rule_id>/restore", methods=["POST"], strict_slashes=False)
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def restore_deduction_rule(rule_id: str):
    rule = g.hrms.deduction_rule.restore(rule_id=rule_id)
    return mapper.to_dto(rule)