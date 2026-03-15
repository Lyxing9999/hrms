from __future__ import annotations

from enum import Enum
from bson import ObjectId

from app.contexts.shared.lifecycle.domain import Lifecycle, now_utc
from app.contexts.hrms.domain.attendance import AttendanceStatus
from app.contexts.hrms.domain.overtime import OvertimeRequest


class PayrollRunStatus(str, Enum):
    DRAFT = "draft"
    FINALIZED = "finalized"
    PAID = "paid"


class PayslipStatus(str, Enum):
    GENERATED = "generated"
    PAID = "paid"


class PayrollRun:
    def __init__(
        self,
        *,
        month: str,
        generated_by: ObjectId,
        id: ObjectId | None = None,
        status: PayrollRunStatus | str = PayrollRunStatus.DRAFT,
        lifecycle: Lifecycle | None = None,
    ) -> None:
        self.id = id or ObjectId()
        self.month = (month or "").strip()
        self.generated_by = generated_by
        self.status = PayrollRunStatus(str(status).strip().lower())
        self.lifecycle = lifecycle or Lifecycle()

        if not self.month:
            raise ValueError("Payroll month is required")

    def finalize(self, *, actor_id: ObjectId) -> None:
        if self.status != PayrollRunStatus.DRAFT:
            raise ValueError("Only draft payroll run can be finalized")
        self.status = PayrollRunStatus.FINALIZED
        self.lifecycle.touch(now_utc())

    def mark_paid(self, *, actor_id: ObjectId) -> None:
        if self.status != PayrollRunStatus.FINALIZED:
            raise ValueError("Only finalized payroll run can be marked paid")
        self.status = PayrollRunStatus.PAID
        self.lifecycle.touch(now_utc())

    def is_deleted(self) -> bool:
        return self.lifecycle.is_deleted()

    def soft_delete(self, *, actor_id: ObjectId | str) -> None:
        self.lifecycle.soft_delete(actor_id=str(actor_id))


class Payslip:
    def __init__(
        self,
        *,
        payroll_run_id: ObjectId,
        employee_id: ObjectId,
        month: str,
        base_salary: float,
        payable_working_days: int,
        paid_holiday_days: int,
        unpaid_leave_days: int,
        total_ot_hours: float,
        ot_payment: float,
        total_deductions: float,
        net_salary: float,
        id: ObjectId | None = None,
        status: PayslipStatus | str = PayslipStatus.GENERATED,
        lifecycle: Lifecycle | None = None,
    ) -> None:
        self.id = id or ObjectId()
        self.payroll_run_id = payroll_run_id
        self.employee_id = employee_id
        self.month = month
        self.base_salary = float(base_salary)
        self.payable_working_days = int(payable_working_days)
        self.paid_holiday_days = int(paid_holiday_days)
        self.unpaid_leave_days = int(unpaid_leave_days)
        self.total_ot_hours = float(total_ot_hours)
        self.ot_payment = float(ot_payment)
        self.total_deductions = float(total_deductions)
        self.net_salary = float(net_salary)
        self.status = PayslipStatus(str(status).strip().lower())
        self.lifecycle = lifecycle or Lifecycle()

    def mark_paid(self, *, actor_id: ObjectId) -> None:
        self.status = PayslipStatus.PAID
        self.lifecycle.touch(now_utc())

    def is_deleted(self) -> bool:
        return self.lifecycle.is_deleted()


class PayrollCalculator:
    """
    Domain service.

    Assumptions:
    - Monthly salary is distributed using expected_working_days in the payroll month.
    - Paid public holiday with no attendance => no deduction.
    - Weekend/public holiday work is handled through approved OT.
    """

    def __init__(self, *, expected_working_days: int) -> None:
        if expected_working_days <= 0:
            raise ValueError("expected_working_days must be positive")
        self.expected_working_days = expected_working_days

    def daily_salary(self, basic_salary: float) -> float:
        return float(basic_salary) / float(self.expected_working_days)

    def calculate_late_deduction(
        self,
        *,
        daily_salary: float,
        late_minutes: int,
        deduction_rules: list,
    ) -> float:
        if late_minutes <= 0:
            return 0.0

        active_rules = [r for r in deduction_rules if r.is_active and not r.is_deleted()]
        for rule in sorted(active_rules, key=lambda r: r.min_minutes):
            if rule.applies_to(late_minutes):
                return rule.calculate_deduction(daily_salary)
        return 0.0

    def calculate_attendance_deductions(
        self,
        *,
        attendances: list,
        basic_salary: float,
        deduction_rules: list,
    ) -> float:
        daily_salary = self.daily_salary(basic_salary)
        total = 0.0

        for attendance in attendances:
            status = attendance.status

            if status == AttendanceStatus.ABSENT:
                total += daily_salary
                continue

            if status == AttendanceStatus.WRONG_LOCATION_REJECTED:
                total += daily_salary
                continue

            total += self.calculate_late_deduction(
                daily_salary=daily_salary,
                late_minutes=attendance.late_minutes,
                deduction_rules=deduction_rules,
            )

        return total

    def calculate_ot_payment(self, *, overtime_requests: list[OvertimeRequest]) -> tuple[float, float]:
        total_hours = 0.0
        total_payment = 0.0

        for ot in overtime_requests:
            if not ot.is_payable():
                continue
            total_hours += ot.approved_hours
            total_payment += ot.calculated_payment

        return total_hours, total_payment

    def calculate_net_salary(
        self,
        *,
        basic_salary: float,
        attendances: list,
        overtime_requests: list[OvertimeRequest],
        deduction_rules: list,
    ) -> dict:
        total_deductions = self.calculate_attendance_deductions(
            attendances=attendances,
            basic_salary=basic_salary,
            deduction_rules=deduction_rules,
        )
        total_ot_hours, ot_payment = self.calculate_ot_payment(
            overtime_requests=overtime_requests
        )

        net_salary = float(basic_salary) + ot_payment - total_deductions

        return {
            "base_salary": float(basic_salary),
            "total_ot_hours": total_ot_hours,
            "ot_payment": ot_payment,
            "total_deductions": total_deductions,
            "net_salary": net_salary,
        }