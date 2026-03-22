from __future__ import annotations


class GetWrongLocationReportQuery:
    def __init__(self, *, attendance_repository) -> None:
        self.attendance_repository = attendance_repository

    def execute(
        self,
        *,
        page: int = 1,
        page_size: int = 10,
        start_date=None,
        end_date=None,
    ):
        if hasattr(self.attendance_repository, "list_wrong_location_cases"):
            return self.attendance_repository.list_wrong_location_cases(
                start_date=start_date,
                end_date=end_date,
                page=page,
                limit=page_size,
            )

        items, total = self.attendance_repository.list_attendances(
            start_date=start_date,
            end_date=end_date,
            page=1,
            limit=5000,
        )

        filtered = [
            x for x in items
            if x.get("status") in {"wrong_location_pending", "wrong_location_rejected"}
            or x.get("wrong_location_reason")
        ]

        filtered.sort(key=lambda x: x.get("check_in_time"), reverse=True)

        start = (page - 1) * page_size
        end = start + page_size
        return filtered[start:end], len(filtered)