from __future__ import annotations

from app.contexts.hrms.errors.employee_exceptions import (
    EmployeeLinkedAccountRequiredException,
    EmployeeNotFoundException,
)


class ChangeEmployeeAccountPasswordUseCase:
    def __init__(self, *, employee_repository, user_management_service) -> None:
        self.employee_repository = employee_repository
        self.user_management_service = user_management_service

    def execute(self, *, employee_id: str, new_password: str) -> dict:
        employee = self.employee_repository.find_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundException(employee_id)

        user_id = employee.get("user_id")
        if not user_id:
            raise EmployeeLinkedAccountRequiredException(str(employee["_id"]))

        self.user_management_service.change_password(
            user_id=user_id,
            new_password=new_password,
        )

        return {
            "employee_id": str(employee["_id"]),
            "user_id": str(user_id),
            "message": "Password updated successfully",
        }