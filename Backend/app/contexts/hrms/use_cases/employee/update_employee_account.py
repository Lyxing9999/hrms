from __future__ import annotations

from app.contexts.hrms.errors.employee_exceptions import (
    EmployeeLinkedAccountRequiredException,
    EmployeeNotFoundException,
)


class UpdateEmployeeAccountUseCase:
    def __init__(self, *, employee_repository, iam_gateway) -> None:
        self.employee_repository = employee_repository
        self.iam_gateway = iam_gateway

    def execute(
        self,
        *,
        employee_id: str,
        email: str | None = None,
        username: str | None = None,
        password: str | None = None,
    ):
        employee = self.employee_repository.find_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundException(employee_id)

        user_id = employee.get("user_id")
        if not user_id:
            raise EmployeeLinkedAccountRequiredException(str(employee["_id"]))

        return self.iam_gateway.update_user_for_employee(
            user_id=user_id,
            email=email,
            username=username,
            password=password,
        )