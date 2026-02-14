# app/contexts/hrms/services/deduction_rule_service.py
from __future__ import annotations
from bson import ObjectId
from pymongo.database import Database

from app.contexts.hrms.read_models.deduction_rule_read_model import DeductionRuleReadModel
from app.contexts.hrms.repositories.deduction_rule_repository import MongoDeductionRuleRepository
from app.contexts.hrms.factories.deduction_rule_factory import DeductionRuleFactory
from app.contexts.hrms.mapper.deduction_rule_mapper import DeductionRuleMapper
from app.contexts.hrms.domain.deduction_rule import DeductionRule, DeductionType
from app.contexts.shared.lifecycle.filters import ShowDeleted
from app.contexts.shared.lifecycle.domain import now_utc
from app.contexts.shared.model_converter import mongo_converter


class DeductionRuleNotFoundException(Exception):
    def __init__(self, rule_id: str):
        super().__init__(f"Deduction rule not found: {rule_id}")


class DeductionRuleService:
    def __init__(self, db: Database):
        self.db = db
        self._read = DeductionRuleReadModel(db)
        self._repo = MongoDeductionRuleRepository(db["deduction_rules"])
        self._mapper = DeductionRuleMapper()
        self._factory = DeductionRuleFactory(self._read)

    def _oid(self, v: str | ObjectId | None) -> ObjectId | None:
        return mongo_converter.convert_to_object_id(v)

    # -------------------------
    # LIST
    # -------------------------
    def list_rules(
        self,
        *,
        page: int = 1,
        page_size: int = 10,
        rule_type: str | None = None,
        is_active: bool | None = None,
        show_deleted: ShowDeleted = "active",
    ) -> tuple[list[DeductionRule], int]:
        items, total = self._read.get_page(
            page=page,
            page_size=page_size,
            rule_type=rule_type,
            is_active=is_active,
            show_deleted=show_deleted,
        )
        domains = [self._mapper.to_domain(x) for x in items]
        return domains, int(total)

    # -------------------------
    # GET ONE
    # -------------------------
    def get_rule(self, rule_id: str | ObjectId, *, show_deleted: ShowDeleted = "active") -> DeductionRule:
        raw = self._read.get_by_id(self._oid(rule_id), show_deleted=show_deleted)
        if not raw:
            raise DeductionRuleNotFoundException(str(rule_id))
        return self._mapper.to_domain(raw)

    # -------------------------
    # GET RULES BY TYPE
    # -------------------------
    def get_rules_by_type(self, rule_type: str) -> list[DeductionRule]:
        """Get all active rules for a specific type (late, absent, early_leave)"""
        items = self._read.get_rules_by_type(rule_type, show_deleted="active")
        return [self._mapper.to_domain(x) for x in items]

    # -------------------------
    # GET ACTIVE RULES
    # -------------------------
    def get_active_rules(self) -> list[DeductionRule]:
        """Get all active deduction rules"""
        items = self._read.get_active_rules(show_deleted="active")
        return [self._mapper.to_domain(x) for x in items]

    # -------------------------
    # FIND APPLICABLE RULE
    # -------------------------
    def find_applicable_rule(self, rule_type: str, minutes: int) -> DeductionRule | None:
        """Find the deduction rule that applies to given minutes"""
        rules = self.get_rules_by_type(rule_type)
        for rule in rules:
            if rule.applies_to(minutes):
                return rule
        return None

    # -------------------------
    # CALCULATE DEDUCTION
    # -------------------------
    def calculate_deduction(self, rule_type: str, minutes: int, daily_salary: float) -> float:
        """Calculate deduction amount for given minutes and daily salary"""
        rule = self.find_applicable_rule(rule_type, minutes)
        if not rule:
            return 0.0
        return rule.calculate_deduction(daily_salary)

    # -------------------------
    # CREATE
    # -------------------------
    def create_rule(self, payload, *, created_by_user_id: str | ObjectId) -> DeductionRule:
        actor_oid = self._oid(created_by_user_id)
        
        p = payload.model_dump()
        
        rule = self._factory.create_rule(payload=p, created_by=actor_oid)
        saved = self._repo.save(self._mapper.to_persistence(rule))
        
        return saved

    # -------------------------
    # UPDATE
    # -------------------------
    def update_rule(self, rule_id: str | ObjectId, payload, *, actor_id: str | ObjectId) -> DeductionRule:
        rule = self.get_rule(rule_id, show_deleted="active")
        
        p = payload.model_dump(exclude_unset=True)
        
        # Update fields
        if "type" in p and p["type"]:
            rule.type = DeductionType(str(p["type"]).strip().lower())
        
        # Check for overlapping rules if range is being updated
        if "min_minutes" in p or "max_minutes" in p:
            min_min = int(p.get("min_minutes", rule.min_minutes))
            max_min = int(p.get("max_minutes", rule.max_minutes))
            
            # Check for overlaps (excluding current rule)
            existing = self._read.get_overlapping_rule(rule.type.value, min_min, max_min)
            if existing and str(existing["_id"]) != str(rule.id):
                raise ValueError(
                    f"A deduction rule for {rule.type.value} already exists that overlaps with "
                    f"{min_min}-{max_min} minutes range"
                )
            
            # Validate and update range
            from app.contexts.hrms.errors.deduction_exceptions import InvalidDeductionRangeException
            if min_min < 0 or max_min < min_min:
                raise InvalidDeductionRangeException(min_min, max_min)
            
            rule.min_minutes = min_min
            rule.max_minutes = max_min
        
        if "deduction_percentage" in p:
            rule.update_percentage(float(p["deduction_percentage"]))
        
        if "is_active" in p:
            if p["is_active"]:
                rule.activate()
            else:
                rule.deactivate()
        
        rule.lifecycle.touch(now_utc())
        
        updated = self._repo.update(self._oid(rule.id), self._mapper.to_persistence(rule))
        if not updated:
            raise DeductionRuleNotFoundException(str(rule_id))
        
        return updated

    # -------------------------
    # SOFT DELETE
    # -------------------------
    def soft_delete_rule(self, rule_id: str | ObjectId, *, actor_id: str | ObjectId) -> DeductionRule:
        rule = self.get_rule(rule_id, show_deleted="active")
        
        rule.soft_delete(actor_id=actor_id)
        
        updated = self._repo.update(self._oid(rule.id), self._mapper.to_persistence(rule))
        if not updated:
            raise DeductionRuleNotFoundException(str(rule_id))
        
        return updated

    # -------------------------
    # RESTORE
    # -------------------------
    def restore_rule(self, rule_id: str | ObjectId) -> DeductionRule:
        rule = self.get_rule(rule_id, show_deleted="deleted_only")
        
        rule.lifecycle.restore()
        
        updated = self._repo.update(self._oid(rule.id), self._mapper.to_persistence(rule))
        if not updated:
            raise DeductionRuleNotFoundException(str(rule_id))
        
        return updated
