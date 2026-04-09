# app/contexts/hrms/errors/holiday_exceptions.py
from app.contexts.core.errors import AppBaseException


class PublicHolidayNotFoundException(AppBaseException):
    def __init__(self, holiday_id: str):
        super().__init__(
            message=f"Public holiday with ID '{holiday_id}' not found",
            error_code="PUBLIC_HOLIDAY_NOT_FOUND",
            status_code=404,
        )


class DuplicateHolidayDateException(AppBaseException):
    def __init__(self, date: str):
        super().__init__(
            message=f"A holiday already exists on {date}",
            error_code="DUPLICATE_HOLIDAY_DATE",
            status_code=409,
        )


class PublicHolidayDeletedException(AppBaseException):
    def __init__(self, holiday_id: str):
        super().__init__(
            message=f"Public holiday '{holiday_id}' has been deleted",
            error_code="PUBLIC_HOLIDAY_DELETED",
            status_code=410,
        )


class HolidayNameRequiredException(AppBaseException):
    def __init__(self):
        super().__init__(
            message="Holiday name is required",
            error_code="HOLIDAY_NAME_REQUIRED",
            status_code=400,
        )
