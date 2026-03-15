from __future__ import annotations


class GetEmployeeQuery:
    def __init__(self, *, employee_repository) -> None:
        self.employee_repository = employee_repository

    def execute(self, *, employee_id: str):
        return self.employee_repository.find_by_id(employee_id)