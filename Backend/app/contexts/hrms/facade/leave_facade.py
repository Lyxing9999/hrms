from __future__ import annotations


class LeaveFacade:
    def __init__(
        self,
        *,
        submit_leave_request,
        approve_leave_request,
    ) -> None:
        self._submit_leave_request = submit_leave_request
        self._approve_leave_request = approve_leave_request

    def submit(self, **kwargs):
        return self._submit_leave_request.execute(**kwargs)

    def approve(self, **kwargs):
        return self._approve_leave_request.execute(**kwargs)