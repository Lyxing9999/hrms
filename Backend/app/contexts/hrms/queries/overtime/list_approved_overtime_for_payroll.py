from __future__ import annotations


class ListApprovedOvertimeForPayrollQuery:
    def __init__(self, *, overtime_repository) -> None:
        self.overtime_repository = overtime_repository

    def execute(self, *, start_date=None, end_date=None):
        return self.overtime_repository.list_approved_for_payroll(
            start_date=start_date,
            end_date=end_date,
        )