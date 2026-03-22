from __future__ import annotations


class GetDefaultWorkingScheduleQuery:
    def __init__(self, *, working_schedule_repository) -> None:
        self.working_schedule_repository = working_schedule_repository

    def execute(self):
        return self.working_schedule_repository.find_default()