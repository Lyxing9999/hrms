from __future__ import annotations


class ListApprovedOvertimeForPayrollQuery:
    def __init__(self, *, overtime_read_model) -> None:
        self.overtime_read_model = overtime_read_model

    def execute(
        self,
        *,
        start_date: str | None = None,
        end_date: str | None = None,
        employee_id: str | None = None,
    ):
        return self.overtime_read_model.list_approved_for_payroll(
            start_date=start_date,
            end_date=end_date,
            employee_id=employee_id,
        )