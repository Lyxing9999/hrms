# app/contexts/hrms/errors/attendance_exceptions.py
from app.contexts.core.errors import AppBaseException


class AttendanceNotFoundException(AppBaseException):
    def __init__(self, attendance_id):
        super().__init__(f"Attendance record with ID {attendance_id} not found", 404)


class AttendanceDeletedException(AppBaseException):
    def __init__(self, attendance_id):
        super().__init__(f"Attendance record {attendance_id} has been deleted", 400)


class AttendanceAlreadyCheckedOutException(AppBaseException):
    def __init__(self, attendance_id):
        super().__init__(f"Attendance {attendance_id} already has check-out time", 400)


class InvalidCheckOutTimeException(AppBaseException):
    def __init__(self, attendance_id):
        super().__init__(f"Check-out time cannot be before check-in time for attendance {attendance_id}", 400)


class AlreadyCheckedInTodayException(AppBaseException):
    def __init__(self, employee_id):
        super().__init__(f"Employee {employee_id} has already checked in today", 400)


class LocationValidationException(AppBaseException):
    def __init__(self, message: str):
        super().__init__(message, 400)
