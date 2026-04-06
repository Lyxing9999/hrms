from __future__ import annotations


class CancelOvertimeRequestUseCase:
    def __init__(self, *, overtime_repository) -> None:
        self.overtime_repository = overtime_repository

    def execute(self, *, overtime_id, actor_id):
        ot = self.overtime_repository.find_by_id(overtime_id)
        if not ot:
            raise ValueError("Overtime request not found")

        if str(ot.employee_id) != str(actor_id):
            raise ValueError("You can only cancel your own overtime request")

        ot.cancel(actor_id=actor_id)
        return self.overtime_repository.save(ot)