from __future__ import annotations


class GetPayrollRunQuery:
    def __init__(self, *, payroll_run_repository) -> None:
        self.payroll_run_repository = payroll_run_repository

    def execute(self, *, payroll_run_id):
        return self.payroll_run_repository.find_by_id(payroll_run_id)