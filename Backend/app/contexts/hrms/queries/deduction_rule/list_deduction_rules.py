from __future__ import annotations


class ListDeductionRulesQuery:
    def __init__(self, *, deduction_rule_repository) -> None:
        self.deduction_rule_repository = deduction_rule_repository

    def execute(
        self,
        *,
        type: str | None = None,
        is_active: bool | None = None,
        include_deleted: bool = False,
        deleted_only: bool = False,
        page: int = 1,
        page_size: int = 10,
    ):
        return self.deduction_rule_repository.list_rules(
            type=type,
            is_active=is_active,
            include_deleted=include_deleted,
            deleted_only=deleted_only,
            page=page,
            page_size=page_size,
        )