from __future__ import annotations


class OvertimeFacade:
    def __init__(
        self,
        *,
        submit_ot_request,
        approve_ot_request,
        reject_ot_request,
    ) -> None:
        self._submit_ot_request = submit_ot_request
        self._approve_ot_request = approve_ot_request
        self._reject_ot_request = reject_ot_request

    def submit(self, **kwargs):
        return self._submit_ot_request.execute(**kwargs)

    def approve(self, **kwargs):
        return self._approve_ot_request.execute(**kwargs)

    def reject(self, **kwargs):
        return self._reject_ot_request.execute(**kwargs)