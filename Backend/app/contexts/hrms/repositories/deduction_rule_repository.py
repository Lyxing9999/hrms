from __future__ import annotations

from bson import ObjectId
from pymongo.database import Database

from app.contexts.hrms.domain.deduction_rule import DeductionRule
from app.contexts.hrms.mapper.deduction_rule_mapper import DeductionRuleMapper
from app.contexts.hrms.errors.deduction_exceptions import DeductionRuleNotFoundException


class MongoDeductionRuleRepository:
    def __init__(self, db: Database):
        self.collection = db["hr_deduction_rules"]
        self.mapper = DeductionRuleMapper()

    def save(self, rule: DeductionRule) -> DeductionRule:
        doc = self.mapper.to_persistence(rule)
        self.collection.replace_one({"_id": doc["_id"]}, doc, upsert=True)
        return rule

    def find_by_id(self, rule_id: ObjectId) -> DeductionRule:
        doc = self.collection.find_one({"_id": rule_id})
        if not doc:
            raise DeductionRuleNotFoundException(rule_id)
        return self.mapper.to_domain(doc)

    def list_rules(
        self,
        *,
        type: str | None = None,
        is_active: bool | None = None,
        include_deleted: bool = False,
        deleted_only: bool = False,
    ) -> list[DeductionRule]:
        query = {}

        if type:
            query["type"] = type
        if is_active is not None:
            query["is_active"] = is_active

        if deleted_only:
            query["lifecycle.deleted_at"] = {"$ne": None}
        elif not include_deleted:
            query["lifecycle.deleted_at"] = None

        docs = self.collection.find(query).sort([("type", 1), ("min_minutes", 1)])
        return [self.mapper.to_domain(doc) for doc in docs]

    def list_active(self, *, type: str | None = None) -> list[DeductionRule]:
        query = {
            "is_active": True,
            "lifecycle.deleted_at": None,
        }
        if type:
            query["type"] = type

        docs = self.collection.find(query).sort("min_minutes", 1)
        return [self.mapper.to_domain(doc) for doc in docs]

    def delete(self, rule_id: ObjectId) -> None:
        self.collection.delete_one({"_id": rule_id})