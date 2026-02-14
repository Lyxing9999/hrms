# app/contexts/hrms/factories/work_location_factory.py
from bson import ObjectId

from app.contexts.hrms.domain.work_location import WorkLocation


class WorkLocationFactory:
    def __init__(self, location_read_model):
        self._read = location_read_model

    def create_location(self, *, payload: dict, created_by: str | ObjectId | None) -> WorkLocation:
        name = (payload.get("name") or "").strip()
        
        # Check if name already exists
        existing = self._read.get_by_name(name)
        if existing:
            raise ValueError(f"Work location with name '{name}' already exists")
        
        return WorkLocation(
            name=name,
            address=payload.get("address", ""),
            latitude=float(payload["latitude"]),
            longitude=float(payload["longitude"]),
            radius_meters=int(payload.get("radius_meters", 100)),
            is_active=payload.get("is_active", True),
            created_by=created_by,
        )
