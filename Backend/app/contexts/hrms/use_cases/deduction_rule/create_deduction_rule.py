from __future__ import annotations

from app.contexts.hrms.domain.deduction_rule import DeductionRule
from app.contexts.shared.model_converter import mongo_converter


class CreateDeductionRuleUseCase:
    def __init__(self, *, deduction_rule_repository) -> None:
        self.deduction_rule_repository = deduction_rule_repository

    def execute(self, *, payload, created_by_user_id: str):
        rule = DeductionRule(
            type=payload.type,
            min_minutes=payload.min_minutes,
            max_minutes=payload.max_minutes,
            deduction_percentage=payload.deduction_percentage,
            is_active=payload.is_active,
            created_by=mongo_converter.convert_to_object_id(created_by_user_id),
        )
        return self.deduction_rule_repository.save(rule)