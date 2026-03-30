# app/contexts/hrms/use_cases/work_location/create_work_location.py
from __future__ import annotations

from bson import ObjectId

from app.contexts.hrms.domain.work_location import WorkLocation


class CreateWorkLocationUseCase:
    def __init__(self, *, work_location_repository) -> None:
        self.work_location_repository = work_location_repository

    def execute(self, *, payload, created_by_user_id: str):
        location = WorkLocation(
            name=payload.name,
            address=payload.address,
            latitude=payload.latitude,
            longitude=payload.longitude,
            radius_meters=payload.radius_meters,
            is_active=payload.is_active,
            created_by=ObjectId(created_by_user_id),
        )
        return self.work_location_repository.create(location)