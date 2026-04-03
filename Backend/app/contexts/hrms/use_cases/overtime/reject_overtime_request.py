from __future__ import annotations


class RejectOvertimeRequestUseCase:
    def __init__(self, *, overtime_repository) -> None:
        self.overtime_repository = overtime_repository

    def execute(self, *, overtime_id, manager_id, comment: str | None = None):
        ot = self.overtime_repository.find_by_id(overtime_id)
        if not ot:
            raise ValueError("Overtime request not found")

        ot.reject(
            manager_id=manager_id,
            comment=comment,
        )

        return self.overtime_repository.save(ot)