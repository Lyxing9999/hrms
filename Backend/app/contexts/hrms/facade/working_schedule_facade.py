from __future__ import annotations


class WorkingScheduleFacade:
    def __init__(
        self,
        *,
        create_working_schedule,
        update_working_schedule,
        set_default_working_schedule,
        soft_delete_working_schedule,
        restore_working_schedule,
        list_working_schedules,
        get_working_schedule,
        get_default_working_schedule,
    ) -> None:
        self._create_working_schedule = create_working_schedule
        self._update_working_schedule = update_working_schedule
        self._set_default_working_schedule = set_default_working_schedule
        self._soft_delete_working_schedule = soft_delete_working_schedule
        self._restore_working_schedule = restore_working_schedule
        self._list_working_schedules = list_working_schedules
        self._get_working_schedule = get_working_schedule
        self._get_default_working_schedule = get_default_working_schedule

    def create(self, **kwargs):
        return self._create_working_schedule.execute(**kwargs)

    def update(self, **kwargs):
        return self._update_working_schedule.execute(**kwargs)

    def set_default(self, **kwargs):
        return self._set_default_working_schedule.execute(**kwargs)

    def soft_delete(self, **kwargs):
        return self._soft_delete_working_schedule.execute(**kwargs)

    def restore(self, **kwargs):
        return self._restore_working_schedule.execute(**kwargs)

    def list(self, **kwargs):
        return self._list_working_schedules.execute(**kwargs)

    def get(self, **kwargs):
        return self._get_working_schedule.execute(**kwargs)

    def get_default(self, **kwargs):
        return self._get_default_working_schedule.execute(**kwargs)
