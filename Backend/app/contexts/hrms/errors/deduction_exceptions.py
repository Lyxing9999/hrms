# app/contexts/hrms/errors/deduction_exceptions.py
from app.contexts.core.errors import AppBaseException


class DeductionRuleNotFoundException(AppBaseException):
    def __init__(self, rule_id: str):
        super().__init__(
            message=f"Deduction rule with ID '{rule_id}' not found",
            error_code="DEDUCTION_RULE_NOT_FOUND",
            status_code=404,
        )


class InvalidDeductionRangeException(AppBaseException):
    def __init__(self, min_minutes: int, max_minutes: int):
        super().__init__(
            message=f"Invalid deduction range: min={min_minutes}, max={max_minutes}. Max must be >= min and both must be >= 0",
            error_code="INVALID_DEDUCTION_RANGE",
            status_code=400,
        )


class InvalidDeductionPercentageException(AppBaseException):
    def __init__(self, percentage: float):
        super().__init__(
            message=f"Invalid deduction percentage: {percentage}%. Must be between 0 and 100",
            error_code="INVALID_DEDUCTION_PERCENTAGE",
            status_code=400,
        )


class DeductionRuleDeletedException(AppBaseException):
    def __init__(self, rule_id: str):
        super().__init__(
            message=f"Deduction rule '{rule_id}' has been deleted",
            error_code="DEDUCTION_RULE_DELETED",
            status_code=410,
        )
