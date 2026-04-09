from __future__ import annotations


class GetDeductionRuleQuery:
    def __init__(self, *, deduction_rule_repository) -> None:
        self.deduction_rule_repository = deduction_rule_repository

    def execute(self, *, rule_id):
        return self.deduction_rule_repository.find_by_id(rule_id)