from __future__ import annotations

from app.contexts.hrms.errors.overtime_exceptions import OvertimeOwnershipRequiredException

class CancelOvertimeRequestUseCase:
    def __init__(self, *, overtime_repository) -> None:
        self.overtime_repository = overtime_repository

    def execute(self, *, overtime_id, actor_id):
        ot = self.overtime_repository.find_by_id(overtime_id)

        if str(ot.employee_id) != str(actor_id):
            raise OvertimeOwnershipRequiredException(
                actor_id=str(actor_id),
                overtime_employee_id=str(ot.employee_id),
            )

        ot.cancel(actor_id=actor_id)
        return self.overtime_repository.save(ot)