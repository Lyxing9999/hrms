from __future__ import annotations


class GetOvertimeRequestQuery:
    def __init__(self, *, overtime_repository) -> None:
        self.overtime_repository = overtime_repository

    def execute(self, *, overtime_id):
        ot = self.overtime_repository.find_by_id(overtime_id)
        if not ot:
            raise ValueError("Overtime request not found")
        return ot