from __future__ import annotations

from bson import ObjectId
from pymongo.database import Database

from app.contexts.hrms.domain.deduction_rule import DeductionRule
from app.contexts.hrms.mapper.deduction_rule_mapper import DeductionRuleMapper


class MongoDeductionRuleRepository:
    def __init__(self, db: Database):
        self.collection = db["hr_deduction_rules"]
        self.mapper = DeductionRuleMapper()

    @staticmethod
    def _oid(v) -> ObjectId | None:
        if v is None:
            return None
        if isinstance(v, ObjectId):
            return v
        return ObjectId(v)

    def save(self, rule: DeductionRule) -> DeductionRule:
        doc = self.mapper.to_persistence(rule)
        self.collection.replace_one({"_id": doc["_id"]}, doc, upsert=True)
        return self.find_by_id(doc["_id"])

    def find_by_id(self, rule_id) -> DeductionRule:
        doc = self.collection.find_one({"_id": self._oid(rule_id)})
        if not doc:
            raise ValueError("Deduction rule not found")
        return self.mapper.to_domain(doc)

    def list_rules(
        self,
        *,
        type: str | None = None,
        is_active: bool | None = None,
        include_deleted: bool = False,
        deleted_only: bool = False,
        page: int = 1,
        page_size: int = 10,
    ) -> tuple[list[DeductionRule], int]:
        query = {}

        if type:
            query["type"] = type

        if is_active is not None:
            query["is_active"] = is_active

        if deleted_only:
            query["lifecycle.deleted_at"] = {"$ne": None}
        elif not include_deleted:
            query["lifecycle.deleted_at"] = None

        total = self.collection.count_documents(query)
        skip = (page - 1) * page_size

        docs = list(
            self.collection.find(query)
            .sort([("type", 1), ("min_minutes", 1)])
            .skip(skip)
            .limit(page_size)
        )
        return [self.mapper.to_domain(x) for x in docs], total

    def find_applicable_rule(self, *, type: str, minutes: int) -> DeductionRule | None:
        docs = list(
            self.collection.find({
                "type": type,
                "is_active": True,
                "lifecycle.deleted_at": None,
            }).sort("min_minutes", 1)
        )

        for doc in docs:
            rule = self.mapper.to_domain(doc)
            if rule.applies_to(minutes):
                return rule
        return None