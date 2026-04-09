from __future__ import annotations


class GetMyLeaveBalanceQuery:
    def __init__(self, *, leave_repository) -> None:
        self.leave_repository = leave_repository

    def execute(self, *, employee_id):
        items, _ = self.leave_repository.list_requests(
            employee_id=employee_id,
            page=1,
            page_size=500,
        )

        used_paid_days = sum(
            x.total_days()
            for x in items
            if (
                (x.status.value if hasattr(x.status, "value") else str(x.status)) == "approved"
                and bool(x.is_paid)
            )
        )

        annual_entitlement = 18  # change later if policy becomes configurable
        remaining_days = max(annual_entitlement - used_paid_days, 0)

        return {
            "annual_entitlement": annual_entitlement,
            "used_days": used_paid_days,
            "remaining_days": remaining_days,
        }