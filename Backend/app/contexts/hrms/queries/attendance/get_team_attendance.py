from __future__ import annotations


class GetTeamAttendanceQuery:
    def __init__(self, *, employee_repository, attendance_repository) -> None:
        self.employee_repository = employee_repository
        self.attendance_repository = attendance_repository

    def execute(
        self,
        *,
        manager_user_id,
        status: str | None = None,
        start_date=None,
        end_date=None,
        page: int = 1,
        page_size: int = 10,
    ):
        employees, _total = self.employee_repository.list_employees(
            manager_user_id=manager_user_id,
            page=1,
            limit=1000,
        )

        employee_ids = [x["_id"] for x in employees]
        if not employee_ids:
            return [], 0

        if hasattr(self.attendance_repository, "list_by_employee_ids"):
            return self.attendance_repository.list_by_employee_ids(
                employee_ids=employee_ids,
                start_date=start_date,
                end_date=end_date,
                status=status,
                page=page,
                limit=page_size,
            )

        # fallback: merge manually
        all_items = []
        for employee_id in employee_ids:
            items, _ = self.attendance_repository.list_attendances(
                employee_id=employee_id,
                start_date=start_date,
                end_date=end_date,
                status=status,
                page=1,
                limit=1000,
            )
            all_items.extend(items)

        all_items.sort(key=lambda x: x.get("check_in_time"), reverse=True)

        start = (page - 1) * page_size
        end = start + page_size
        return all_items[start:end], len(all_items)