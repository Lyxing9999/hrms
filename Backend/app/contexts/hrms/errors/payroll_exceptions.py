    # app/contexts/hrms/errors/payroll_exceptions.py
from bson import ObjectId
from app.contexts.core.errors import AppBaseException, ErrorSeverity, ErrorCategory

class PayrollAlreadyFinalizedException(AppBaseException):
    def __init__(self, payroll_run_id: ObjectId, status: str):
        super().__init__(
            message=f"Payroll run {payroll_run_id} cannot be changed (status={status})",
            error_code="PAYROLL_ALREADY_FINALIZED",
            severity=ErrorSeverity.MEDIUM,
            category=ErrorCategory.BUSINESS_LOGIC,
            details={"payroll_run_id": str(payroll_run_id), "status": status},
            hint="Only draft payroll can be recalculated/finalized",
            recoverable=True,
        )

class PayrollRunDeletedException(AppBaseException):
    def __init__(self, payroll_run_id: ObjectId):
        super().__init__(
            message=f"Payroll run {payroll_run_id} is deleted",
            error_code="PAYROLL_RUN_DELETED",
            severity=ErrorSeverity.LOW,
            category=ErrorCategory.BUSINESS_LOGIC,
            details={"payroll_run_id": str(payroll_run_id)},
            hint="Restore payroll run or generate a new one",
            recoverable=True,
        )

class PayrollNotFoundException(AppBaseException):
    def __init__(self, payroll_run_id: str):
        super().__init__(
            message=f"Payroll run {payroll_run_id} not found",
            error_code="PAYROLL_NOT_FOUND",
            status_code=404,
            severity=ErrorSeverity.LOW,
            category=ErrorCategory.BUSINESS_LOGIC,
            context={"payroll_run_id": payroll_run_id},
            user_message="Payroll run not found",
            hint="Generate payroll first",
            recoverable=True,
        )



class PayrollRunNotFoundException(AppBaseException):
    pass


class PayslipNotFoundException(AppBaseException):
    pass