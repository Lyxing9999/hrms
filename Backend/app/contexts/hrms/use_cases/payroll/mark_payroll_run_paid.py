from __future__ import annotations


class MarkPayrollRunPaidUseCase:
    def __init__(self, *, payroll_run_repository, payslip_repository) -> None:
        self.payroll_run_repository = payroll_run_repository
        self.payslip_repository = payslip_repository

    def execute(self, *, payroll_run_id, actor_id):
        run = self.payroll_run_repository.find_by_id(payroll_run_id)
        run.mark_paid(actor_id=actor_id)
        saved_run = self.payroll_run_repository.save(run)

        payslips, _ = self.payslip_repository.list_payslips(
            payroll_run_id=payroll_run_id,
            page=1,
            page_size=5000,
        )
        for payslip in payslips:
            payslip.mark_paid(actor_id=actor_id)
            self.payslip_repository.save(payslip)

        return saved_run