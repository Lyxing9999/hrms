from __future__ import annotations

from bson import ObjectId

from app.contexts.hrms.domain.deduction_rule import DeductionRule
from app.contexts.shared.lifecycle.domain import Lifecycle
from app.contexts.shared.lifecycle.dto import LifecycleDTO
from app.contexts.hrms.data_transfer.response.deduction_rule_response import DeductionRuleDTO
from app.contexts.shared.model_converter import mongo_converter


class DeductionRuleMapper:
    @staticmethod
    def _oid(v) -> ObjectId | None:
        return mongo_converter.convert_to_object_id(v)

    @staticmethod
    def _sid(v) -> str | None:
        if v is None:
            return None
        return str(v)

    @staticmethod
    def to_domain(data: dict) -> DeductionRule:
        if not isinstance(data, dict):
            raise TypeError(f"to_domain expected dict, got {type(data)}")

        lc_src = data.get("lifecycle") or {}
        lifecycle = Lifecycle(
            created_at=lc_src.get("created_at") or data.get("created_at"),
            updated_at=lc_src.get("updated_at") or data.get("updated_at"),
            deleted_at=lc_src.get("deleted_at") or data.get("deleted_at"),
            deleted_by=lc_src.get("deleted_by") or data.get("deleted_by"),
        )

        return DeductionRule(
            id=DeductionRuleMapper._oid(data.get("_id") or data.get("id")),
            type=data.get("type"),
            min_minutes=int(data.get("min_minutes", 0)),
            max_minutes=int(data["max_minutes"]) if data.get("max_minutes") is not None else None,
            deduction_percentage=float(data.get("deduction_percentage", 0)),
            is_active=bool(data.get("is_active", True)),
            created_by=DeductionRuleMapper._oid(data.get("created_by")),
            lifecycle=lifecycle,
        )

    @staticmethod
    def to_persistence(rule: DeductionRule) -> dict:
        if not isinstance(rule, DeductionRule):
            raise TypeError(f"to_persistence expected DeductionRule, got {type(rule)}")

        lc = rule.lifecycle
        doc = {
            "type": rule.type.value if hasattr(rule.type, "value") else str(rule.type),
            "min_minutes": rule.min_minutes,
            "max_minutes": rule.max_minutes,
            "deduction_percentage": rule.deduction_percentage,
            "is_active": rule.is_active,
            "created_by": DeductionRuleMapper._oid(rule.created_by),
            "lifecycle": {
                "created_at": lc.created_at,
                "updated_at": lc.updated_at,
                "deleted_at": lc.deleted_at,
                "deleted_by": DeductionRuleMapper._oid(lc.deleted_by),
            },
        }

        if rule.id:
            doc["_id"] = DeductionRuleMapper._oid(rule.id)

        return doc

    @staticmethod
    def to_dto(rule: DeductionRule) -> DeductionRuleDTO:
        lc = rule.lifecycle
        return DeductionRuleDTO(
            id=str(rule.id),
            type=rule.type.value if hasattr(rule.type, "value") else str(rule.type),
            min_minutes=rule.min_minutes,
            max_minutes=rule.max_minutes,
            deduction_percentage=rule.deduction_percentage,
            is_active=rule.is_active,
            created_by=DeductionRuleMapper._sid(rule.created_by),
            lifecycle=LifecycleDTO(
                created_at=lc.created_at,
                updated_at=lc.updated_at,
                deleted_at=lc.deleted_at,
                deleted_by=lc.deleted_by,
            ),
        )