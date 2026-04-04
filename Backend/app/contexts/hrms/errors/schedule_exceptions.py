# app/contexts/hrms/errors/schedule_exceptions.py
from app.contexts.core.errors import AppBaseException, ErrorSeverity, ErrorCategory


class InvalidWorkingHoursException(AppBaseException):
    def __init__(self, start_time, end_time):
        super().__init__(
            error_code="INVALID_WORKING_HOURS",
            message=f"End time ({end_time}) must be after start time ({start_time})",
            status_code=400,
            details={"start_time": str(start_time), "end_time": str(end_time)}
        )


class InvalidWorkingDaysException(AppBaseException):
    def __init__(self, working_days):
        super().__init__(
            error_code="INVALID_WORKING_DAYS",
            message=f"Invalid working days: {working_days}. Must be integers 0-6 (Monday-Sunday)",
            status_code=400,
            details={"working_days": working_days}
        )


class WorkingScheduleNotFoundException(AppBaseException):
    def __init__(self, schedule_id):
        super().__init__(
            error_code="SCHEDULE_NOT_FOUND",
            message=f"Working schedule not found: {schedule_id}",
            status_code=404,
            details={"schedule_id": str(schedule_id)}
        )


class DefaultScheduleRequiredException(AppBaseException):
    def __init__(self):
        super().__init__(
            error_code="DEFAULT_SCHEDULE_REQUIRED",
            message="At least one default working schedule must exist",
            status_code=400
        )


class WorkingScheduleDeletedException(AppBaseException):
    def __init__(self, schedule_id):
        super().__init__(
            error_code="SCHEDULE_DELETED",
            message=f"Working schedule is deleted: {schedule_id}",
            status_code=400,
            details={"schedule_id": str(schedule_id)},
        )
