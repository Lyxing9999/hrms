# app/contexts/hrms/errors/employee_exceptions.py
from bson import ObjectId
from datetime import date as date_type
from app.contexts.core.errors import AppBaseException, ErrorSeverity, ErrorCategory

class EmployeeNotFoundException(AppBaseException):
    def __init__(self, employee_id: str):
        super().__init__(
            message=f"Employee '{employee_id}' not found",
            error_code="EMPLOYEE_NOT_FOUND",
            status_code=404,
            severity=ErrorSeverity.LOW,
            category=ErrorCategory.BUSINESS_LOGIC,
            user_message="Employee not found.",
            context={"employee_id": employee_id},
            recoverable=True,
        )

class EmployeeDeletedException(AppBaseException):
    def __init__(self, employee_id: ObjectId):
        super().__init__(
            message=f"Employee {employee_id} is deleted",
            error_code="EMPLOYEE_DELETED",
            severity=ErrorSeverity.MEDIUM,
            category=ErrorCategory.BUSINESS_LOGIC,
            details={"employee_id": str(employee_id)},
            hint="Restore employee before linking account",
            recoverable=True,
        )

class EmployeeCodeAlreadyExistsException(AppBaseException):
    def __init__(self, employee_code: str):
        super().__init__(
            message=f"Employee code '{employee_code}' already exists",
            error_code="EMPLOYEE_CODE_EXISTS",
            severity=ErrorSeverity.MEDIUM,
            category=ErrorCategory.BUSINESS_LOGIC,
            user_message="Employee code already exists.",
            details={"employee_code": employee_code},
            recoverable=True,
        )

class ContractRequiredException(AppBaseException):
    def __init__(self, employee_id: ObjectId):
        super().__init__(
            message="Contract is required for contract employees",
            error_code="EMPLOYEE_CONTRACT_REQUIRED",
            severity=ErrorSeverity.LOW,
            category=ErrorCategory.VALIDATION,
            details={"employee_id": str(employee_id)},
            recoverable=True,
        )

class ContractDateInvalidException(AppBaseException):
    def __init__(self, start_date: date_type | None, end_date: date_type | None):
        super().__init__(
            message=f"Invalid contract dates: {start_date} -> {end_date}",
            error_code="EMPLOYEE_CONTRACT_DATE_INVALID",
            severity=ErrorSeverity.LOW,
            category=ErrorCategory.VALIDATION,
            details={"start_date": str(start_date), "end_date": str(end_date)},
            hint="contract.end_date must be >= contract.start_date",
            recoverable=True,
        )


class EmployeeInactiveException(AppBaseException):
    def __init__(self, employee_id: str, status: str):
        super().__init__(
            message=f"Employee '{employee_id}' is not active (status={status})",
            error_code="EMPLOYEE_INACTIVE",
            status_code=403,
            severity=ErrorSeverity.MEDIUM,
            category=ErrorCategory.BUSINESS_LOGIC,
            user_message="Employee account is not active.",
            details={"employee_id": employee_id, "status": status},
            hint="Activate employee status before attendance operations.",
            recoverable=True,
        )


class EmployeeScheduleNotAssignedException(AppBaseException):
    def __init__(self, employee_id: str):
        super().__init__(
            message=f"Employee '{employee_id}' has no assigned working schedule",
            error_code="EMPLOYEE_SCHEDULE_NOT_ASSIGNED",
            status_code=400,
            severity=ErrorSeverity.LOW,
            category=ErrorCategory.BUSINESS_LOGIC,
            user_message="Working schedule is required before attendance operations.",
            details={"employee_id": employee_id},
            hint="Assign a working schedule to the employee.",
            recoverable=True,
        )