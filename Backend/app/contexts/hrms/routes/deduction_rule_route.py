# app/contexts/hrms/routes/deduction_rule_route.py
from flask import Blueprint, request, g
from app.contexts.shared.model_converter import pydantic_converter, mongo_converter
from app.contexts.shared.decorators.response_decorator import wrap_response
from app.contexts.iam.auth.jwt_utils import login_required
from app.contexts.core.security.auth_utils import get_current_staff_id
import math

from app.contexts.hrms.data_transfer.request.deduction_rule_request import (
    DeductionRuleCreateSchema,
    DeductionRuleUpdateSchema,
)
from app.contexts.hrms.data_transfer.response.deduction_rule_response import (
    DeductionRuleDTO,
    DeductionRulePaginatedDTO,
)

deduction_rule_bp = Blueprint("deduction_rule_bp", __name__)


# -------------------------
# LIST RULES
# -------------------------
@deduction_rule_bp.route("/deduction-rules", methods=["GET"])
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def list_rules():
    page = max(int(request.args.get("page") or 1), 1)
    page_size = min(max(int(request.args.get("limit") or 10), 1), 100)
    
    rule_type = request.args.get("type")
    is_active_str = request.args.get("is_active")
    is_active = None if is_active_str is None else is_active_str.lower() == "true"
    
    include_deleted = (request.args.get("include_deleted") or "false").lower() == "true"
    deleted_only = (request.args.get("deleted_only") or "false").lower() == "true"
    show_deleted = "all" if include_deleted else ("deleted_only" if deleted_only else "active")
    
    items, total = g.hrms.deduction_rule_service.list_rules(
        page=page,
        page_size=page_size,
        rule_type=rule_type,
        is_active=is_active,
        show_deleted=show_deleted,
    )
    
    items_dto = [mongo_converter.doc_to_dto(g.hrms.deduction_rule_service._mapper.to_persistence(item), DeductionRuleDTO) for item in items]
    total_pages = max(1, math.ceil(int(total) / page_size))
    
    return DeductionRulePaginatedDTO(
        items=items_dto,
        total=int(total),
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


# -------------------------
# GET ACTIVE RULES
# -------------------------
@deduction_rule_bp.route("/deduction-rules/active", methods=["GET"])
@login_required(allowed_roles=["hr_admin", "manager"])
@wrap_response
def get_active_rules():
    rules = g.hrms.deduction_rule_service.get_active_rules()
    items_dto = [mongo_converter.doc_to_dto(g.hrms.deduction_rule_service._mapper.to_persistence(r), DeductionRuleDTO) for r in rules]
    
    return {"items": items_dto}


# -------------------------
# GET RULES BY TYPE
# -------------------------
@deduction_rule_bp.route("/deduction-rules/type/<rule_type>", methods=["GET"])
@login_required(allowed_roles=["hr_admin", "manager"])
@wrap_response
def get_rules_by_type(rule_type: str):
    rules = g.hrms.deduction_rule_service.get_rules_by_type(rule_type)
    items_dto = [mongo_converter.doc_to_dto(g.hrms.deduction_rule_service._mapper.to_persistence(r), DeductionRuleDTO) for r in rules]
    
    return {"items": items_dto, "type": rule_type}


# -------------------------
# GET SINGLE RULE
# -------------------------
@deduction_rule_bp.route("/deduction-rules/<rule_id>", methods=["GET"])
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def get_rule(rule_id: str):
    rule = g.hrms.deduction_rule_service.get_rule(rule_id)
    return mongo_converter.doc_to_dto(g.hrms.deduction_rule_service._mapper.to_persistence(rule), DeductionRuleDTO)


# -------------------------
# CREATE RULE
# -------------------------
@deduction_rule_bp.route("/deduction-rules", methods=["POST"])
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def create_rule():
    staff_id = get_current_staff_id()
    
    payload = pydantic_converter.convert_to_model(request.json, DeductionRuleCreateSchema)
    rule = g.hrms.deduction_rule_service.create_rule(payload, created_by_user_id=staff_id)
    return mongo_converter.doc_to_dto(g.hrms.deduction_rule_service._mapper.to_persistence(rule), DeductionRuleDTO)


# -------------------------
# UPDATE RULE
# -------------------------
@deduction_rule_bp.route("/deduction-rules/<rule_id>", methods=["PATCH"])
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def update_rule(rule_id: str):
    staff_id = get_current_staff_id()
    
    payload = pydantic_converter.convert_to_model(request.json, DeductionRuleUpdateSchema)
    rule = g.hrms.deduction_rule_service.update_rule(rule_id, payload, actor_id=staff_id)
    return mongo_converter.doc_to_dto(g.hrms.deduction_rule_service._mapper.to_persistence(rule), DeductionRuleDTO)


# -------------------------
# SOFT DELETE RULE
# -------------------------
@deduction_rule_bp.route("/deduction-rules/<rule_id>/soft-delete", methods=["DELETE"])
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def soft_delete_rule(rule_id: str):
    staff_id = get_current_staff_id()
    
    rule = g.hrms.deduction_rule_service.soft_delete_rule(rule_id, actor_id=staff_id)
    return mongo_converter.doc_to_dto(g.hrms.deduction_rule_service._mapper.to_persistence(rule), DeductionRuleDTO)


# -------------------------
# RESTORE RULE
# -------------------------
@deduction_rule_bp.route("/deduction-rules/<rule_id>/restore", methods=["POST"])
@login_required(allowed_roles=["hr_admin"])
@wrap_response
def restore_rule(rule_id: str):
    rule = g.hrms.deduction_rule_service.restore_rule(rule_id)
    return mongo_converter.doc_to_dto(g.hrms.deduction_rule_service._mapper.to_persistence(rule), DeductionRuleDTO)
