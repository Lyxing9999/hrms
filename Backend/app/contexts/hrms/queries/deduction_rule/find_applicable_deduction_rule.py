from __future__ import annotations


class FindApplicableDeductionRuleQuery:
    def __init__(self, *, deduction_rule_repository) -> None:
        self.deduction_rule_repository = deduction_rule_repository

    def execute(self, *, type: str, minutes: int):
        return self.deduction_rule_repository.find_applicable_rule(
            type=type,
            minutes=minutes,
        )