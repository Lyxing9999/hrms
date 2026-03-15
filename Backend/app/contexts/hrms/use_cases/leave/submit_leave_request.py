from __future__ import annotations

from datetime import date as date_type


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

    def execute(
        self,
        *,
        employee_id: str,
        leave_type: str,
        start_date: date_type,
        end_date: date_type,
        reason: str,
        is_paid: bool,
    ) -> dict:
        employee = self._get_employee(employee_id)
        contract_start, contract_end = self._extract_contract_range(employee)

        leave_request = self._build_leave_request(
            employee=employee,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            reason=reason,
            contract_start=contract_start,
            contract_end=contract_end,
            is_paid=is_paid,
        )

        self._save_leave_request(leave_request)
        self._write_audit_log(leave_request=leave_request, employee=employee)

        return self._build_result(leave_request)

    def _get_employee(self, employee_id: str):
        # TODO
        return self.employee_repository.get_by_id(employee_id)

    def _extract_contract_range(self, employee):
        # TODO: adapt based on your employee model
        # TODO: for permanent employee, you may decide very wide contract range
        if employee.contract:
            return employee.contract["start_date"], employee.contract["end_date"]

        # TODO: replace this fallback with your actual rule
        raise ValueError("Employee contract range is required")

    def _build_leave_request(
        self,
        *,
        employee,
        leave_type: str,
        start_date: date_type,
        end_date: date_type,
        reason: str,
        contract_start,
        contract_end,
        is_paid: bool,
    ):
        # TODO: import and create LeaveRequest
        leave_request = None
        return leave_request

    def _save_leave_request(self, leave_request) -> None:
        # TODO
        self.leave_repository.save(leave_request)

    def _write_audit_log(self, *, leave_request, employee) -> None:
        # TODO
        if self.audit_log_repository is None:
            return

    def _build_result(self, leave_request) -> dict:
        return {
            "leave_request_id": str(leave_request.id),
            "status": leave_request.status.value,
            "total_days": leave_request.total_days(),
        }