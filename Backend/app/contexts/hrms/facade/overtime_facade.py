from __future__ import annotations


class OvertimeFacade:
    def __init__(
        self,
        *,
        create_overtime_request,
        approve_overtime_request,
        reject_overtime_request,
        cancel_overtime_request=None,
        list_overtime_requests=None,
        get_overtime_request=None,
        list_my_overtime_requests=None,
        list_approved_overtime_for_payroll=None,
    ) -> None:
        self._create_overtime_request = create_overtime_request
        self._approve_overtime_request = approve_overtime_request
        self._reject_overtime_request = reject_overtime_request
        self._cancel_overtime_request = cancel_overtime_request
        self._list_overtime_requests = list_overtime_requests
        self._get_overtime_request = get_overtime_request
        self._list_my_overtime_requests = list_my_overtime_requests
        self._list_approved_overtime_for_payroll = list_approved_overtime_for_payroll

    def create(self, **kwargs):
        return self._create_overtime_request.execute(**kwargs)

    def approve(self, **kwargs):
        return self._approve_overtime_request.execute(**kwargs)

    def reject(self, **kwargs):
        return self._reject_overtime_request.execute(**kwargs)

    def cancel(self, **kwargs):
        if not self._cancel_overtime_request:
            raise NotImplementedError("cancel_overtime_request is not configured")
        return self._cancel_overtime_request.execute(**kwargs)

    def list(self, **kwargs):
        if not self._list_overtime_requests:
            raise NotImplementedError("list_overtime_requests is not configured")
        return self._list_overtime_requests.execute(**kwargs)

    def get(self, **kwargs):
        if not self._get_overtime_request:
            raise NotImplementedError("get_overtime_request is not configured")
        return self._get_overtime_request.execute(**kwargs)

    def list_my(self, **kwargs):
        if not self._list_my_overtime_requests:
            raise NotImplementedError("list_my_overtime_requests is not configured")
        return self._list_my_overtime_requests.execute(**kwargs)

    def list_approved_for_payroll(self, **kwargs):
        if not self._list_approved_overtime_for_payroll:
            raise NotImplementedError("list_approved_overtime_for_payroll is not configured")
        return self._list_approved_overtime_for_payroll.execute(**kwargs)