# app/contexts/hrms/domain/payroll.py
from __future__ import annotations

from enum import Enum
from bson import ObjectId
from app.contexts.shared.lifecycle.domain import Lifecycle, now_utc
from app.contexts.hrms.errors.payroll_exceptions import PayrollRunDeletedException, PayrollAlreadyFinalizedException

class PayrollRunStatus(str, Enum):
    DRAFT = "draft"
    FINALIZED = "finalized"
    PAID = "paid"

class PayslipStatus(str, Enum):
    GENERATED = "generated"
    PAID = "paid"

class PayrollRun:
    def __init__(self, *, month: str, generated_by: ObjectId, id: ObjectId | None = None,
                 status: PayrollRunStatus | str = PayrollRunStatus.DRAFT, lifecycle: Lifecycle | None = None) -> None:
        self.id = id or ObjectId()
        self.month = month
        self.generated_by = generated_by
        self.status = PayrollRunStatus(str(status).strip().lower())
        self.lifecycle = lifecycle or Lifecycle()

    def finalize(self, *, actor_id: ObjectId) -> None:
        if self.is_deleted():
            raise PayrollRunDeletedException(self.id)
        if self.status != PayrollRunStatus.DRAFT:
            raise PayrollAlreadyFinalizedException(self.id, self.status.value)
        self.status = PayrollRunStatus.FINALIZED
        self.lifecycle.touch(now_utc())

    def mark_paid(self, *, actor_id: ObjectId) -> None:
        if self.is_deleted():
            raise PayrollRunDeletedException(self.id)
        self.status = PayrollRunStatus.PAID
        self.lifecycle.touch(now_utc())

    def is_deleted(self) -> bool:
        return self.lifecycle.is_deleted()

class Payslip:
    def __init__(
        self,
        *,
        payroll_run_id: ObjectId,
        employee_id: ObjectId,
        month: str,
        base_salary: float,
        ot_payment: float,
        deductions: float,
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
        self.ot_payment = float(ot_payment)
        self.deductions = float(deductions)
        self.net_salary = float(net_salary)

        self.status = PayslipStatus(str(status).strip().lower())
        self.lifecycle = lifecycle or Lifecycle()

    def mark_paid(self, *, actor_id: ObjectId) -> None:
        self.status = PayslipStatus.PAID
        self.lifecycle.touch(now_utc())

    def is_deleted(self) -> bool:
        return self.lifecycle.is_deleted()