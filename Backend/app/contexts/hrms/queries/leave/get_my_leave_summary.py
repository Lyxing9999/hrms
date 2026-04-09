from __future__ import annotations


class GetMyLeaveSummaryQuery:
    def __init__(self, *, leave_repository) -> None:
        self.leave_repository = leave_repository

    def execute(self, *, employee_id):
        items, _ = self.leave_repository.list_requests(
            employee_id=employee_id,
            page=1,
            page_size=500,
        )

        total_requests = len(items)
        pending = sum(1 for x in items if str(x.status.value if hasattr(x.status, "value") else x.status) == "pending")
        approved = sum(1 for x in items if str(x.status.value if hasattr(x.status, "value") else x.status) == "approved")
        rejected = sum(1 for x in items if str(x.status.value if hasattr(x.status, "value") else x.status) == "rejected")
        cancelled = sum(1 for x in items if str(x.status.value if hasattr(x.status, "value") else x.status) == "cancelled")
        total_approved_days = sum(x.total_days() for x in items if str(x.status.value if hasattr(x.status, "value") else x.status) == "approved")

        return {
            "total_requests": total_requests,
            "pending": pending,
            "approved": approved,
            "rejected": rejected,
            "cancelled": cancelled,
            "total_approved_days": total_approved_days,
        }