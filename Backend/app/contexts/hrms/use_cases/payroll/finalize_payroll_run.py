from __future__ import annotations


class FinalizePayrollRunUseCase:
    def __init__(self, *, payroll_run_repository) -> None:
        self.payroll_run_repository = payroll_run_repository

    def execute(self, *, payroll_run_id, actor_id):
        run = self.payroll_run_repository.find_by_id(payroll_run_id)
        run.finalize(actor_id=actor_id)
        return self.payroll_run_repository.save(run)