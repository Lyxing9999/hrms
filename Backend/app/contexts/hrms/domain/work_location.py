from __future__ import annotations

from math import radians, sin, cos, sqrt, atan2
from bson import ObjectId

from app.contexts.shared.lifecycle.domain import Lifecycle, now_utc


class WorkLocation:
    def __init__(
        self,
        *,
        name: str,
        address: str,
        latitude: float,
        longitude: float,
        radius_meters: int,
        id: ObjectId | None = None,
        is_active: bool = True,
        created_by: ObjectId | None = None,
        lifecycle: Lifecycle | None = None,
    ) -> None:
        self.id = id or ObjectId()
        self.name = (name or "").strip()
        self.address = (address or "").strip()
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.radius_meters = int(radius_meters)
        self.is_active = bool(is_active)
        self.created_by = created_by
        self.lifecycle = lifecycle or Lifecycle()

        if not self.name:
            raise ValueError("Location name is required")
        if not (-90 <= self.latitude <= 90):
            raise ValueError("Invalid latitude")
        if not (-180 <= self.longitude <= 180):
            raise ValueError("Invalid longitude")
        if not (10 <= self.radius_meters <= 1000):
            raise ValueError("Radius must be between 10 and 1000 meters")

    def distance_meters(self, latitude: float, longitude: float) -> float:
        earth_radius = 6371000
        lat1 = radians(self.latitude)
        lon1 = radians(self.longitude)
        lat2 = radians(latitude)
        lon2 = radians(longitude)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return earth_radius * c

    def contains(self, latitude: float, longitude: float) -> bool:
        return self.distance_meters(latitude, longitude) <= self.radius_meters

    def activate(self) -> None:
        self.is_active = True
        self.lifecycle.touch(now_utc())

    def deactivate(self) -> None:
        self.is_active = False
        self.lifecycle.touch(now_utc())

    def update_coordinates(self, latitude: float, longitude: float) -> None:
        if not (-90 <= latitude <= 90):
            raise ValueError("Invalid latitude")
        if not (-180 <= longitude <= 180):
            raise ValueError("Invalid longitude")
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.lifecycle.touch(now_utc())

    def update_radius(self, radius_meters: int) -> None:
        if not (10 <= radius_meters <= 1000):
            raise ValueError("Radius must be between 10 and 1000 meters")
        self.radius_meters = int(radius_meters)
        self.lifecycle.touch(now_utc())

    def is_deleted(self) -> bool:
        return self.lifecycle.is_deleted()

    def soft_delete(self, *, actor_id: ObjectId | str) -> None:
        self.lifecycle.soft_delete(actor_id=str(actor_id))