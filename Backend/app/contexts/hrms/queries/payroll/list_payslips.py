from __future__ import annotations


class ListPayslipsQuery:
    def __init__(self, *, payslip_repository) -> None:
        self.payslip_repository = payslip_repository

    def execute(
        self,
        *,
        payroll_run_id=None,
        employee_id=None,
        month: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ):
        return self.payslip_repository.list_payslips(
            payroll_run_id=payroll_run_id,
            employee_id=employee_id,
            month=month,
            page=page,
            page_size=page_size,
        )