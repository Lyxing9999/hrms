# app/contexts/hrms/errors/leave_exceptions.py
from datetime import date as date_type
from bson import ObjectId
from app.contexts.core.errors import AppBaseException, ErrorSeverity, ErrorCategory

class LeaveDateRangeInvalidException(AppBaseException):
    def __init__(self, start_date: date_type, end_date: date_type):
        super().__init__(
            message=f"Invalid leave range: {start_date} -> {end_date}",
            error_code="LEAVE_RANGE_INVALID",
            severity=ErrorSeverity.LOW,
            category=ErrorCategory.BUSINESS_LOGIC,
            details={"start_date": str(start_date), "end_date": str(end_date)},
            hint="end_date must be >= start_date",
            recoverable=True,
        )

class LeaveOutsideContractException(AppBaseException):
    def __init__(self, start_date: date_type, end_date: date_type, cstart: date_type, cend: date_type):
        super().__init__(
            message=f"Leave {start_date}->{end_date} outside contract {cstart}->{cend}",
            error_code="LEAVE_OUTSIDE_CONTRACT",
            severity=ErrorSeverity.MEDIUM,
            category=ErrorCategory.BUSINESS_LOGIC,
            details={"leave_start": str(start_date), "leave_end": str(end_date), "contract_start": str(cstart), "contract_end": str(cend)},
            hint="Leave dates must be within contract period",
            recoverable=True,
        )

class LeaveAlreadyReviewedException(AppBaseException):
    def __init__(self, leave_id: ObjectId, status: str):
        super().__init__(
            message=f"Leave {leave_id} already reviewed (status={status})",
            error_code="LEAVE_ALREADY_REVIEWED",
            severity=ErrorSeverity.LOW,
            category=ErrorCategory.BUSINESS_LOGIC,
            details={"leave_id": str(leave_id), "status": status},
            hint="Only pending leave can be approved/rejected/cancelled",
            recoverable=True,
        )

class LeaveRequestDeletedException(AppBaseException):
    def __init__(self, leave_id: ObjectId):
        super().__init__(
            message=f"Leave {leave_id} is deleted",
            error_code="LEAVE_DELETED",
            severity=ErrorSeverity.LOW,
            category=ErrorCategory.BUSINESS_LOGIC,
            details={"leave_id": str(leave_id)},
            hint="Restore leave or create new leave",
            recoverable=True,
        )

class LeaveNotFoundException(AppBaseException):
    def __init__(self, leave_id: str):
        super().__init__(
            message=f"Leave {leave_id} not found",
            error_code="LEAVE_NOT_FOUND",
            status_code=404,
            severity=ErrorSeverity.LOW,
            category=ErrorCategory.BUSINESS_LOGIC,
            context={"leave_id": leave_id},
            user_message="The requested leave does not exist.",
            hint="Check leave ID",
            recoverable=True,
        )