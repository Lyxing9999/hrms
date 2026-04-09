from __future__ import annotations

from app.contexts.hrms.domain.leave import LeaveRequest, LeaveType


class SubmitLeaveRequestUseCase:
    def __init__(
        self,
        *,
        employee_repository,
        leave_repository,
        audit_log_repository=None,
    ) -> None:
        self.employee_repository = employee_repository
        self.leave_repository = leave_repository
        self.audit_log_repository = audit_log_repository

    def execute(self, *, employee_id, payload):
        employee = self.employee_repository.find_by_id(employee_id)
        if not employee:
            raise ValueError("Employee not found")

        if str(employee.get("status") or "inactive") != "active":
            raise ValueError("Employee is not active")

        employment_type = str(employee.get("employment_type") or "").strip().lower()
        contract = employee.get("contract") or {}

        contract_start = contract.get("start_date")
        contract_end = contract.get("end_date")

        if employment_type == "contract":
            if not contract_start or not contract_end:
                raise ValueError("Employee contract period is required for contract employees")

            if payload.start_date < contract_start or payload.end_date > contract_end:
                raise ValueError("Leave request is outside contract period")
        else:
            contract_start = payload.start_date
            contract_end = payload.end_date
        overlap = self.leave_repository.find_overlapping_approved_or_pending(
            employee_id=employee["_id"],
            start_date=payload.start_date,
            end_date=payload.end_date,
        )
        if overlap:
            raise ValueError("Overlapping leave request already exists")

        is_paid = payload.leave_type in {
            LeaveType.ANNUAL.value,
            LeaveType.SICK.value,
        }

        leave = LeaveRequest(
            employee_id=employee["_id"],
            leave_type=payload.leave_type,
            start_date=payload.start_date,
            end_date=payload.end_date,
            reason=payload.reason,
            contract_start=contract_start,
            contract_end=contract_end,
            is_paid=is_paid,
        )

        return self.leave_repository.save(leave)