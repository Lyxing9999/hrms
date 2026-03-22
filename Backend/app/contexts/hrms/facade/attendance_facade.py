from __future__ import annotations


class AttendanceFacade:
    def __init__(
        self,
        *,
        check_in_employee,
        check_out_employee,
        approve_wrong_location,
        get_my_attendance,
        list_attendance,
        get_team_attendance,
        get_wrong_location_report,
    ) -> None:
        self._check_in_employee = check_in_employee
        self._check_out_employee = check_out_employee
        self._approve_wrong_location = approve_wrong_location
        self._get_my_attendance = get_my_attendance
        self._list_attendance = list_attendance
        self._get_team_attendance = get_team_attendance
        self._get_wrong_location_report = get_wrong_location_report

    def check_in(self, **kwargs):
        return self._check_in_employee.execute(**kwargs)

    def check_out(self, **kwargs):
        return self._check_out_employee.execute(**kwargs)

    def approve_wrong_location(self, **kwargs):
        return self._approve_wrong_location.execute(**kwargs)

    def get_my_attendance(self, **kwargs):
        return self._get_my_attendance.execute(**kwargs)

    def list_attendance(self, **kwargs):
        return self._list_attendance.execute(**kwargs)

    def get_team_attendance(self, **kwargs):
        return self._get_team_attendance.execute(**kwargs)

    def get_wrong_location_report(self, **kwargs):
        return self._get_wrong_location_report.execute(**kwargs)