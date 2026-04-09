from __future__ import annotations


class ListPayrollRunsQuery:
    def __init__(self, *, payroll_run_repository) -> None:
        self.payroll_run_repository = payroll_run_repository

    def execute(self, *, page: int = 1, page_size: int = 10):
        return self.payroll_run_repository.list_runs(page=page, page_size=page_size)