from __future__ import annotations




class CreateEmployeeAccountUseCase:
    def __init__(self, *, employee_repository, iam_gateway) -> None:
        self.employee_repository = employee_repository
        self.iam_gateway = iam_gateway

    def execute(self, *, employee_id: str, payload, created_by_user_id):
        employee = self.employee_repository.find_by_id(employee_id)

        if employee.get("user_id"):
            raise ValueError("Employee already linked to account")

        iam_user = self.iam_gateway.create_user_for_employee(
            email=payload.email,
            password=payload.password,
            username=payload.username,
            role=payload.role,
            created_by=created_by_user_id,
        )

        employee = self.employee_repository.update_fields(
            employee["_id"],
            {"user_id": iam_user.id},
        )

        return iam_user, employee