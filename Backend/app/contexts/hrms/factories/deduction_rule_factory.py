# app/contexts/hrms/factories/deduction_rule_factory.py
from bson import ObjectId

from app.contexts.hrms.domain.deduction_rule import DeductionRule, DeductionType


class DeductionRuleFactory:
    def __init__(self, rule_read_model):
        self._read = rule_read_model

    def create_rule(self, *, payload: dict, created_by: str | ObjectId | None) -> DeductionRule:
        rule_type = DeductionType(str(payload["type"]).strip().lower())
        min_minutes = int(payload["min_minutes"])
        max_minutes = int(payload["max_minutes"])
        
        # Check for overlapping rules of the same type
        existing = self._read.get_overlapping_rule(rule_type.value, min_minutes, max_minutes)
        if existing:
            raise ValueError(
                f"A deduction rule for {rule_type.value} already exists that overlaps with "
                f"{min_minutes}-{max_minutes} minutes range"
            )
        
        return DeductionRule(
            type=rule_type,
            min_minutes=min_minutes,
            max_minutes=max_minutes,
            deduction_percentage=float(payload["deduction_percentage"]),
            is_active=payload.get("is_active", True),
            created_by=created_by,
        )
