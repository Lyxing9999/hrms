from typing import Tuple, List, Dict, Any
from bson import ObjectId
from pymongo.database import Database
from app.contexts.shared.lifecycle.filters import by_show_deleted, ShowDeleted
from app.contexts.shared.model_converter import mongo_converter


class DeductionRuleReadModel:
    def __init__(self, db: Database):
        self.collection = db["hr_deduction_rules"]

    def get_by_id(self, rule_id: ObjectId | str, *, show_deleted: ShowDeleted = "active") -> dict | None:
        oid = mongo_converter.convert_to_object_id(rule_id)
        if not oid:
            return None
        return self.collection.find_one(by_show_deleted(show_deleted, {"_id": oid}))

    def get_overlapping_rule(
        self,
        rule_type: str,
        min_minutes: int,
        max_minutes: int,
        *,
        show_deleted: ShowDeleted = "active"
    ) -> dict | None:
        query = by_show_deleted(show_deleted, {
            "type": rule_type.lower(),
            "is_active": True,
            "min_minutes": {"$lte": max_minutes},
            "max_minutes": {"$gte": min_minutes},
        })
        return self.collection.find_one(query)

    def get_rules_by_type(self, rule_type: str, *, show_deleted: ShowDeleted = "active") -> List[dict]:
        query = by_show_deleted(show_deleted, {"type": rule_type.lower(), "is_active": True})
        return list(self.collection.find(query).sort("min_minutes", 1))

    def get_active_rules(self, *, show_deleted: ShowDeleted = "active") -> List[dict]:
        query = by_show_deleted(show_deleted, {"is_active": True})
        return list(self.collection.find(query).sort([("type", 1), ("min_minutes", 1)]))

    def get_page(
        self,
        *,
        page: int = 1,
        page_size: int = 10,
        rule_type: str | None = None,
        is_active: bool | None = None,
        show_deleted: ShowDeleted = "active",
    ) -> Tuple[List[Dict[str, Any]], int]:
        page = max(1, int(page))
        page_size = min(max(1, int(page_size)), 100)
        skip = (page - 1) * page_size

        base: Dict[str, Any] = {}

        if rule_type:
            base["type"] = rule_type.lower()

        if is_active is not None:
            base["is_active"] = is_active

        query = by_show_deleted(show_deleted, base)
        total = self.collection.count_documents(query)

        items = list(
            self.collection.find(query)
            .sort([("type", 1), ("min_minutes", 1)])
            .skip(skip)
            .limit(page_size)
        )
        return items, total