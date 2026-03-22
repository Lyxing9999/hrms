from __future__ import annotations



class FindEmployeeByUserIdQuery:
    def __init__(self, *, employee_repository) -> None:
        self.employee_repository = employee_repository

    def execute(self, *, user_id):
        return self.employee_repository.find_by_user_id(user_id)