from __future__ import annotations

from app.contexts.shared.lifecycle.domain import now_utc


class RestoreDeductionRuleUseCase:
    def __init__(self, *, deduction_rule_repository) -> None:
        self.deduction_rule_repository = deduction_rule_repository

    def execute(self, *, rule_id):
        rule = self.deduction_rule_repository.find_by_id(rule_id)
        rule.lifecycle.deleted_at = None
        rule.lifecycle.deleted_by = None
        rule.lifecycle.touch(now_utc())
        return self.deduction_rule_repository.save(rule)