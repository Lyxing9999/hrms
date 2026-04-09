from __future__ import annotations


class GetMyAttendanceTodayQuery:
    def __init__(self, *, attendance_read_model) -> None:
        self.attendance_read_model = attendance_read_model

    def execute(self, *, employee_id):
        return self.attendance_read_model.find_by_employee_today(employee_id)