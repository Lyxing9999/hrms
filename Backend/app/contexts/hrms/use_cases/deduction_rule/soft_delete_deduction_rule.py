from __future__ import annotations


class SoftDeleteDeductionRuleUseCase:
    def __init__(self, *, deduction_rule_repository) -> None:
        self.deduction_rule_repository = deduction_rule_repository

    def execute(self, *, rule_id, actor_id):
        rule = self.deduction_rule_repository.find_by_id(rule_id)
        rule.soft_delete(actor_id=actor_id)
        return self.deduction_rule_repository.save(rule)