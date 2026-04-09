from __future__ import annotations


class GetPayslipQuery:
    def __init__(self, *, payslip_repository) -> None:
        self.payslip_repository = payslip_repository

    def execute(self, *, payslip_id):
        return self.payslip_repository.find_by_id(payslip_id)