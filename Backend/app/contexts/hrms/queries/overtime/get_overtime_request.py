from __future__ import annotations

from app.contexts.hrms.errors.overtime_exceptions import OvertimeRequestNotFoundException


class GetOvertimeRequestQuery:
    def __init__(self, *, overtime_read_model) -> None:
        self.overtime_read_model = overtime_read_model

    def execute(self, *, overtime_id: str):
        item = self.overtime_read_model.get_by_id(overtime_id)
        if not item:
            raise OvertimeRequestNotFoundException(overtime_id)
        return item