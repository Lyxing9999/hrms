from __future__ import annotations


class GetEmployeeAccountQuery:
    def __init__(self, *, employee_repository, iam_gateway) -> None:
        self.employee_repository = employee_repository
        self.iam_gateway = iam_gateway

    def execute(self, *, employee_id: str):
        employee = self.employee_repository.find_by_id(employee_id)
        if not employee:
            raise ValueError(f"Employee {employee_id} not found")

        user_id = employee.get("user_id")
        if not user_id:
            return None

        return self.iam_gateway.get_account_summary_by_user_id(user_id)