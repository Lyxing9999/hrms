# app/contexts/hrms/facades/work_location_facade.py
from __future__ import annotations


class WorkLocationFacade:
    def __init__(
            self,
            *, 
            create_work_location,
            update_work_location,
            activate_work_location,
            deactivate_work_location,
            soft_delete_work_location,
            restore_work_location,
            list_work_locations,
            get_work_location,
            get_active_work_location
        ) -> None:
        self._create_work_location = create_work_location
        self._update_work_location = update_work_location
        self._activate_work_location = activate_work_location
        self._deactivate_work_location = deactivate_work_location
        self._soft_delete_work_location = soft_delete_work_location
        self._restore_work_location = restore_work_location
        self._list_work_locations = list_work_locations
        self._get_work_location = get_work_location
        self._get_active_work_location = get_active_work_location
        

    def create(self, *, payload, created_by_user_id: str):
        return self._create_work_location.execute(
            payload=payload,
            created_by_user_id=created_by_user_id,
        )

    def update(self, *, location_id: str, payload, actor_id: str):
        return self._update_work_location.execute(
            location_id=location_id,
            payload=payload,
            actor_id=actor_id,
        )

    def activate(self, *, location_id: str, actor_id: str):
        return self._activate_work_location.execute(
            location_id=location_id,
            actor_id=actor_id,
        )

    def deactivate(self, *, location_id: str, actor_id: str):
        return self._deactivate_work_location.execute(
            location_id=location_id,
            actor_id=actor_id,
        )

    def soft_delete(self, *, location_id: str, actor_id: str):
        return self._soft_delete_work_location.execute(
            location_id=location_id,
            actor_id=actor_id,
        )

    def restore(self, *, location_id: str):
        return self._restore_work_location.execute(
            location_id=location_id,
        )

    def list(self, *, q: str = "", status: str = "all"):
        return self._list_work_locations.execute(
            q=q,
            status=status,
        )

    def get(self, *, location_id: str):
        return self._get_work_location.execute(
            location_id=location_id,
        )

    def get_active(self):
        return self._get_active_work_location.execute()