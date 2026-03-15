from app.contexts.core.errors import AppBaseException


from bson import ObjectId


class OvertimeRequestNotFoundException(AppBaseException):
    def __init__(self, overtime_request_id: ObjectId):
        super(overtime_request_id).__init__(
                # TODO
                
                )