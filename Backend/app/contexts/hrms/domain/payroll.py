from __future__ import annotations

from enum import Enum
from bson import ObjectId

from app.contexts.shared.lifecycle.domain import Lifecycle, now_utc
from app.contexts.hrms.domain.attendance import AttendanceStatus
from app.contexts.hrms.domain.overtime import OvertimeRequest
from app.contexts.hrms.domain.deduction_rule import DeductionType
from app.contexts.hrms.errors.payroll_exceptions import (
    PayrollExpectedWorkingDaysInvalidException,
    PayrollFinalizeStateInvalidException,
    PayrollMarkPaidStateInvalidException,
    PayrollMonthRequiredException,
    PayslipMonthRequiredException,
)


class PayrollRunStatus(str, Enum):
    DRAFT = "draft"
    FINALIZED = "finalized"
    PAID = "paid"


class PayslipStatus(str, Enum):
    GENERATED = "generated"
    PAID = "paid"


class PayrollRun:
    @staticmethod
    def _normalize_status(value) -> PayrollRunStatus:
        if isinstance(value, PayrollRunStatus):
            return value
        return PayrollRunStatus(str(value).strip().lower())

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
        self.status = self._normalize_status(status)
        self.lifecycle = lifecycle or Lifecycle()

        if not self.month:
            raise PayrollMonthRequiredException()

    def finalize(self, *, actor_id: ObjectId) -> None:
        if self.status != PayrollRunStatus.DRAFT:
            raise PayrollFinalizeStateInvalidException(str(self.id), str(self.status))
        self.status = PayrollRunStatus.FINALIZED
        self.lifecycle.touch(now_utc())

    def mark_paid(self, *, actor_id: ObjectId) -> None:
        if self.status != PayrollRunStatus.FINALIZED:
            raise PayrollMarkPaidStateInvalidException(str(self.id), str(self.status))
        self.status = PayrollRunStatus.PAID
        self.lifecycle.touch(now_utc())

    def is_deleted(self) -> bool:
        return self.lifecycle.is_deleted()

    def soft_delete(self, *, actor_id: ObjectId | str) -> None:
        self.lifecycle.soft_delete(actor_id=str(actor_id))


class Payslip:
    @staticmethod
    def _normalize_status(value) -> PayslipStatus:
        if isinstance(value, PayslipStatus):
            return value
        return PayslipStatus(str(value).strip().lower())

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
        self.month = (month or "").strip()
        self.base_salary = float(base_salary)
        self.payable_working_days = int(payable_working_days)
        self.paid_holiday_days = int(paid_holiday_days)
        self.unpaid_leave_days = int(unpaid_leave_days)
        self.total_ot_hours = float(total_ot_hours)
        self.ot_payment = float(ot_payment)
        self.total_deductions = float(total_deductions)
        self.net_salary = float(net_salary)
        self.status = self._normalize_status(status)
        self.lifecycle = lifecycle or Lifecycle()

        if not self.month:
            raise PayslipMonthRequiredException()

    def mark_paid(self, *, actor_id: ObjectId) -> None:
        self.status = PayslipStatus.PAID
        self.lifecycle.touch(now_utc())

    def is_deleted(self) -> bool:
        return self.lifecycle.is_deleted()


class PayrollCalculator:
    def __init__(self, *, expected_working_days: int) -> None:
        if expected_working_days <= 0:
            raise PayrollExpectedWorkingDaysInvalidException(expected_working_days)
        self.expected_working_days = expected_working_days

    def daily_salary(self, basic_salary: float) -> float:
        return float(basic_salary) / float(self.expected_working_days)

    def _active_rules_for_type(self, *, deduction_rules: list, type_value: str) -> list:
        result = []
        for rule in deduction_rules:
            rule_type = rule.type.value if hasattr(rule.type, "value") else str(rule.type)
            if rule.is_active and not rule.is_deleted() and rule_type == type_value:
                result.append(rule)
        return sorted(result, key=lambda r: r.min_minutes)

    def calculate_minutes_based_deduction(
        self,
        *,
        daily_salary: float,
        minutes: int,
        deduction_rules: list,
        type_value: str,
    ) -> float:
        if minutes <= 0:
            return 0.0

        active_rules = self._active_rules_for_type(
            deduction_rules=deduction_rules,
            type_value=type_value,
        )
        for rule in active_rules:
            if rule.applies_to(minutes):
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
            status = attendance.status.value if hasattr(attendance.status, "value") else str(attendance.status)
            location_review_status = (
                attendance.location_review_status.value
                if hasattr(attendance.location_review_status, "value")
                else str(attendance.location_review_status)
            )

            if status == AttendanceStatus.HOLIDAY_OFF.value:
                continue

            if status == AttendanceStatus.WEEKEND_OFF.value:
                continue

            if status == AttendanceStatus.ABSENT.value:
                total += daily_salary
                continue

            if location_review_status == "rejected" or status == AttendanceStatus.WRONG_LOCATION_REJECTED.value:
                total += daily_salary
                continue

            total += self.calculate_minutes_based_deduction(
                daily_salary=daily_salary,
                minutes=int(attendance.late_minutes or 0),
                deduction_rules=deduction_rules,
                type_value=DeductionType.LATE.value,
            )

            total += self.calculate_minutes_based_deduction(
                daily_salary=daily_salary,
                minutes=int(attendance.early_leave_minutes or 0),
                deduction_rules=deduction_rules,
                type_value=DeductionType.EARLY_LEAVE.value,
            )

        return total

    def calculate_unpaid_leave_deduction(
        self,
        *,
        basic_salary: float,
        unpaid_leave_days: int,
    ) -> float:
        if unpaid_leave_days <= 0:
            return 0.0
        return self.daily_salary(basic_salary) * float(unpaid_leave_days)

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
        unpaid_leave_days: int = 0,
    ) -> dict:
        attendance_deductions = self.calculate_attendance_deductions(
            attendances=attendances,
            basic_salary=basic_salary,
            deduction_rules=deduction_rules,
        )

        unpaid_leave_deduction = self.calculate_unpaid_leave_deduction(
            basic_salary=basic_salary,
            unpaid_leave_days=unpaid_leave_days,
        )

        total_deductions = attendance_deductions + unpaid_leave_deduction

        total_ot_hours, ot_payment = self.calculate_ot_payment(
            overtime_requests=overtime_requests
        )

        net_salary = float(basic_salary) + ot_payment - total_deductions

        return {
            "base_salary": float(basic_salary),
            "total_ot_hours": total_ot_hours,
            "ot_payment": ot_payment,
            "attendance_deductions": attendance_deductions,
            "unpaid_leave_deduction": unpaid_leave_deduction,
            "total_deductions": total_deductions,
            "net_salary": net_salary,
        }