from __future__ import annotations


class ListEmployeesWithAccountsQuery:
    def __init__(self, *, employee_repository, iam_gateway) -> None:
        self.employee_repository = employee_repository
        self.iam_gateway = iam_gateway

    def execute(self, *, q="", page=1, page_size=10, show_deleted="active"):
        employees, total = self.employee_repository.list_employees(
            q=q,
            page=page,
            page_size=page_size,
            show_deleted=show_deleted,
        )

        user_ids = [x.get("user_id") for x in employees if x.get("user_id")]
        account_map = self.iam_gateway.get_account_summaries_by_user_ids(user_ids)

        items = []
        for employee in employees:
            account = None
            user_id = employee.get("user_id")
            if user_id:
                account = account_map.get(str(user_id))

            items.append({
                "employee": employee,
                "account": account,
            })

        return items, total