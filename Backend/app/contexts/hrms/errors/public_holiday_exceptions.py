from bson import ObjectId
from app.contexts.core.errors import AppBaseException, ErrorSeverity, ErrorCategory







class PublicHolidayNotFoundException(AppBaseException):
    def __init__(self, *arg):
        super().__init__(
                # TODO
                
                )