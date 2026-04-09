from __future__ import annotations


class GetMyOvertimeSummaryQuery:
    def __init__(self, *, overtime_read_model) -> None:
        self.overtime_read_model = overtime_read_model

    def execute(self, *, employee_id):
        return self.overtime_read_model.get_my_summary(
            employee_id=employee_id,
        )