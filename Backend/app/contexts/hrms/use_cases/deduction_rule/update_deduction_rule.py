from __future__ import annotations

from app.contexts.hrms.errors.deduction_exceptions import InvalidDeductionRangeException


class UpdateDeductionRuleUseCase:
    def __init__(self, *, deduction_rule_repository) -> None:
        self.deduction_rule_repository = deduction_rule_repository

    def execute(self, *, rule_id, payload):
        rule = self.deduction_rule_repository.find_by_id(rule_id)

        if payload.min_minutes is not None:
            rule.min_minutes = int(payload.min_minutes)

        if payload.max_minutes is not None or payload.max_minutes is None:
            rule.max_minutes = payload.max_minutes

        if payload.deduction_percentage is not None:
            rule.update_percentage(payload.deduction_percentage)

        if payload.is_active is True:
            rule.activate()
        elif payload.is_active is False:
            rule.deactivate()

        if rule.max_minutes is not None and rule.max_minutes < rule.min_minutes:
            raise InvalidDeductionRangeException(rule.min_minutes, rule.max_minutes)

        return self.deduction_rule_repository.save(rule)