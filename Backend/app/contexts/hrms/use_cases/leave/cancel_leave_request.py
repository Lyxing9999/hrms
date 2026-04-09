from __future__ import annotations

from app.contexts.hrms.errors.leave_exceptions import LeaveCancellationNotAllowedException


class CancelLeaveRequestUseCase:
    def __init__(self, *, leave_repository) -> None:
        self.leave_repository = leave_repository

    def execute(self, *, leave_id, actor_employee_id):
        leave = self.leave_repository.find_by_id(leave_id)

        if str(leave.employee_id) != str(actor_employee_id):
            raise LeaveCancellationNotAllowedException(
                actor_employee_id=str(actor_employee_id),
                leave_employee_id=str(leave.employee_id),
            )

        leave.cancel(actor_id=actor_employee_id)
        return self.leave_repository.save(leave)