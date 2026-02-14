# app/contexts/hrms/domain/work_location.py
from __future__ import annotations
from bson import ObjectId

from app.contexts.shared.lifecycle.domain import Lifecycle, now_utc
from app.contexts.hrms.errors.location_exceptions import (
    InvalidLocationCoordinatesException,
    InvalidRadiusException,
)


class WorkLocation:
    """
    Defines approved work locations for check-in validation.
    Includes GPS coordinates and acceptable radius.
    """
    
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
        
        if not self.name:
            raise ValueError("Location name is required")
        
        # Validate coordinates
        if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
            raise InvalidLocationCoordinatesException(latitude, longitude)
        
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        
        # Validate radius (10m to 1000m)
        if not (10 <= radius_meters <= 1000):
            raise InvalidRadiusException(radius_meters)
        
        self.radius_meters = int(radius_meters)
        self.is_active = bool(is_active)
        self.created_by = created_by
        self.lifecycle = lifecycle or Lifecycle()
    
    def activate(self) -> None:
        """Activate this location"""
        self.is_active = True
        self.lifecycle.touch(now_utc())
    
    def deactivate(self) -> None:
        """Deactivate this location"""
        self.is_active = False
        self.lifecycle.touch(now_utc())
    
    def update_coordinates(self, latitude: float, longitude: float) -> None:
        """Update location coordinates"""
        if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
            raise InvalidLocationCoordinatesException(latitude, longitude)
        
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.lifecycle.touch(now_utc())
    
    def update_radius(self, radius_meters: int) -> None:
        """Update acceptable radius"""
        if not (10 <= radius_meters <= 1000):
            raise InvalidRadiusException(radius_meters)
        
        self.radius_meters = int(radius_meters)
        self.lifecycle.touch(now_utc())
    
    def is_deleted(self) -> bool:
        return self.lifecycle.is_deleted()
    
    def soft_delete(self, *, actor_id: str | ObjectId) -> None:
        """Soft delete the location"""
        self.lifecycle.soft_delete(actor_id=str(actor_id))
