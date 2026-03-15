from __future__ import annotations


class GenerateMonthlyPayrollUseCase:
    def __init__(
        self,
        *,
        employee_repository,
        attendance_repository,
        overtime_repository,
        deduction_rule_repository,
        payroll_run_repository,
        payslip_repository,
        audit_log_repository=None,
        payroll_calculator=None,
    ) -> None:
        self.employee_repository = employee_repository
        self.attendance_repository = attendance_repository
        self.overtime_repository = overtime_repository
        self.deduction_rule_repository = deduction_rule_repository
        self.payroll_run_repository = payroll_run_repository
        self.payslip_repository = payslip_repository
        self.audit_log_repository = audit_log_repository
        self.payroll_calculator = payroll_calculator

    def execute(
        self,
        *,
        month: str,
        generated_by: str,
        expected_working_days: int,
    ) -> dict:
        payroll_run = self._create_payroll_run(
            month=month,
            generated_by=generated_by,
        )

        employees = self._get_active_employees()
        deduction_rules = self._get_active_deduction_rules()

        generated_count = 0
        payslip_ids: list[str] = []

        for employee in employees:
            attendances = self._get_employee_attendances(employee=employee, month=month)
            overtime_requests = self._get_employee_overtime_requests(employee=employee, month=month)

            payroll_result = self._calculate_employee_payroll(
                employee=employee,
                attendances=attendances,
                overtime_requests=overtime_requests,
                deduction_rules=deduction_rules,
                expected_working_days=expected_working_days,
            )

            payslip = self._build_payslip(
                payroll_run=payroll_run,
                employee=employee,
                month=month,
                payroll_result=payroll_result,
                expected_working_days=expected_working_days,
            )

            self._save_payslip(payslip)

            generated_count += 1
            payslip_ids.append(str(payslip.id))

        self._save_payroll_run(payroll_run)
        self._write_audit_log(payroll_run=payroll_run, generated_by=generated_by)

        return self._build_result(
            payroll_run=payroll_run,
            generated_count=generated_count,
            payslip_ids=payslip_ids,
        )

    def _create_payroll_run(self, *, month: str, generated_by: str):
        # TODO: import PayrollRun and create instance
        payroll_run = None
        # TODO: self.payroll_run_repository.save(payroll_run)
        return payroll_run

    def _get_active_employees(self):
        # TODO
        return self.employee_repository.list_active()

    def _get_active_deduction_rules(self):
        # TODO
        return self.deduction_rule_repository.list_active()

    def _get_employee_attendances(self, *, employee, month: str):
        # TODO: replace with your real query method
        return self.attendance_repository.list_by_employee_and_month(
            employee_id=employee.id,
            month=month,
        )

    def _get_employee_overtime_requests(self, *, employee, month: str):
        # TODO: replace with your real query method
        return self.overtime_repository.list_approved_by_employee_and_month(
            employee_id=employee.id,
            month=month,
        )

    def _calculate_employee_payroll(
        self,
        *,
        employee,
        attendances,
        overtime_requests,
        deduction_rules,
        expected_working_days: int,
    ) -> dict:
        # TODO:
        # Option A: use domain PayrollCalculator
        # Option B: inject a calculator service
        # Option C: compute here only temporarily
        #
        # expected return example:
        # {
        #   "base_salary": 0,
        #   "total_ot_hours": 0,
        #   "ot_payment": 0,
        #   "total_deductions": 0,
        #   "net_salary": 0,
        #   "paid_holiday_days": 0,
        #   "unpaid_leave_days": 0,
        # }
        return {
            "base_salary": employee.basic_salary,
            "total_ot_hours": 0.0,
            "ot_payment": 0.0,
            "total_deductions": 0.0,
            "net_salary": employee.basic_salary,
            "paid_holiday_days": 0,
            "unpaid_leave_days": 0,
        }

    def _build_payslip(
        self,
        *,
        payroll_run,
        employee,
        month: str,
        payroll_result: dict,
        expected_working_days: int,
    ):
        # TODO: import and create Payslip
        payslip = None
        return payslip

    def _save_payslip(self, payslip) -> None:
        # TODO
        self.payslip_repository.save(payslip)

    def _save_payroll_run(self, payroll_run) -> None:
        # TODO: maybe already saved during create; adapt to your repo style
        self.payroll_run_repository.save(payroll_run)

    def _write_audit_log(self, *, payroll_run, generated_by: str) -> None:
        # TODO
        if self.audit_log_repository is None:
            return

    def _build_result(self, *, payroll_run, generated_count: int, payslip_ids: list[str]) -> dict:
        return {
            "payroll_run_id": str(payroll_run.id),
            "month": payroll_run.month,
            "status": payroll_run.status.value,
            "generated_count": generated_count,
            "payslip_ids": payslip_ids,
        }