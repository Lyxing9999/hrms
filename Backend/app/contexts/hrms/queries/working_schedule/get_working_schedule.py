from __future__ import annotations


class GetWorkingScheduleQuery:
    def __init__(self, *, working_schedule_repository) -> None:
        self.working_schedule_repository = working_schedule_repository

    def execute(self, *, schedule_id):
        return self.working_schedule_repository.find_by_id(schedule_id)