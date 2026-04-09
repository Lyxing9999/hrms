from __future__ import annotations


class ApproveLeaveRequestUseCase:
    def __init__(self, *, leave_repository, employee_repository, audit_log_repository=None) -> None:
        self.leave_repository = leave_repository
        self.employee_repository = employee_repository
        self.audit_log_repository = audit_log_repository

    def execute(self, *, leave_id, manager_user_id, comment: str | None = None):
        leave = self.leave_repository.find_by_id(leave_id)

        employee = self.employee_repository.find_by_id(leave.employee_id)
        if not employee:
            raise ValueError("Employee not found")

        employee_manager_user_id = employee.get("manager_user_id")
        if employee_manager_user_id and str(employee_manager_user_id) != str(manager_user_id):
            raise ValueError("You can only approve leave requests from your own team")

        leave.approve(manager_id=manager_user_id, comment=comment)
        return self.leave_repository.save(leave)