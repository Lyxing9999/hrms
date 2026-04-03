from __future__ import annotations


class CancelOvertimeRequestUseCase:
    def __init__(self, *, overtime_repository) -> None:
        self.overtime_repository = overtime_repository

    def execute(self, *, overtime_id, actor_id):
        ot = self.overtime_repository.find_by_id(overtime_id)
        if not ot:
            raise ValueError("Overtime request not found")

        ot.cancel(actor_id=actor_id)
        return self.overtime_repository.save(ot)