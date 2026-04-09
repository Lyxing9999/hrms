from __future__ import annotations


class CancelLeaveRequestUseCase:
    def __init__(self, *, leave_repository) -> None:
        self.leave_repository = leave_repository

    def execute(self, *, leave_id, actor_employee_id):
        leave = self.leave_repository.find_by_id(leave_id)

        if str(leave.employee_id) != str(actor_employee_id):
            raise ValueError("You can only cancel your own leave request")

        leave.cancel(actor_id=actor_employee_id)
        return self.leave_repository.save(leave)