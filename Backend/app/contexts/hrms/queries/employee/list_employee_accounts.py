from __future__ import annotations


class ListEmployeeAccountsQuery:
    def __init__(self, *, iam_gateway) -> None:
        self.iam_gateway = iam_gateway

    def execute(
        self,
        *,
        page: int = 1,
        page_size: int = 10,
        search: str = "",
        show_deleted: str = "active",
        status: str | None = None,
    ):
        return self.iam_gateway.get_employee_accounts_page(
            page=page,
            page_size=page_size,
            search=search,
            show_deleted=show_deleted,
            status=status,
        )