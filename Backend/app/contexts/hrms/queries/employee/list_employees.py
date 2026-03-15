from __future__ import annotations


class ListEmployeesQuery:
    def __init__(self, *, employee_repository) -> None:
        self.employee_repository = employee_repository

    def execute(
        self,
        *,
        q: str = "",
        page: int = 1,
        page_size: int = 10,
        show_deleted: str = "active",
    ):
        return self.employee_repository.list_employees(
            q=q,
            page=page,
            page_size=page_size,
            show_deleted=show_deleted,
        )