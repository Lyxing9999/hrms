# app/contexts/hrms/use_cases/work_location/update_work_location.py
from __future__ import annotations

from app.contexts.shared.lifecycle.domain import now_utc


class UpdateWorkLocationUseCase:
    def __init__(self, *, work_location_repository) -> None:
        self.work_location_repository = work_location_repository

    def execute(self, *, location_id: str, payload, actor_id: str):
        location = self.work_location_repository.find_by_id(location_id)

        if payload.name is not None:
            location.name = payload.name.strip()

        if payload.address is not None:
            location.address = payload.address.strip()

        if payload.latitude is not None and payload.longitude is not None:
            location.update_coordinates(payload.latitude, payload.longitude)
        elif payload.latitude is not None or payload.longitude is not None:
            raise ValueError("Both latitude and longitude are required when updating coordinates")

        if payload.radius_meters is not None:
            location.update_radius(payload.radius_meters)

        if payload.is_active is not None:
            if payload.is_active:
                location.activate()
            else:
                location.deactivate()

        location.lifecycle.touch(now_utc())
        return self.work_location_repository.save(location)