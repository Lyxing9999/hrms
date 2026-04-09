from __future__ import annotations


class GetOvertimePayrollSummaryQuery:
    def __init__(self, *, overtime_read_model) -> None:
        self.overtime_read_model = overtime_read_model

    def execute(
        self,
        *,
        start_date: str | None = None,
        end_date: str | None = None,
    ):
        return self.overtime_read_model.get_payroll_summary(
            start_date=start_date,
            end_date=end_date,
        )