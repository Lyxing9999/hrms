# app/contexts/hrms/services/work_location_service.py
from __future__ import annotations
from bson import ObjectId
from pymongo.database import Database

from app.contexts.hrms.read_models.work_location_read_model import WorkLocationReadModel
from app.contexts.hrms.repositories.work_location_repository import MongoWorkLocationRepository
from app.contexts.hrms.factories.work_location_factory import WorkLocationFactory
from app.contexts.hrms.mapper.work_location_mapper import WorkLocationMapper
from app.contexts.hrms.domain.work_location import WorkLocation
from app.contexts.shared.lifecycle.filters import ShowDeleted
from app.contexts.shared.lifecycle.domain import now_utc
from app.contexts.shared.model_converter import mongo_converter


class WorkLocationNotFoundException(Exception):
    def __init__(self, location_id: str):
        super().__init__(f"Work location not found: {location_id}")


class WorkLocationService:
    def __init__(self, db: Database):
        self.db = db
        self._read = WorkLocationReadModel(db)
        self._repo = MongoWorkLocationRepository(db["work_locations"])
        self._mapper = WorkLocationMapper()
        self._factory = WorkLocationFactory(self._read)

    def _oid(self, v: str | ObjectId | None) -> ObjectId | None:
        return mongo_converter.convert_to_object_id(v)

    # -------------------------
    # LIST
    # -------------------------
    def list_locations(
        self,
        *,
        q: str = "",
        page: int = 1,
        page_size: int = 10,
        is_active: bool | None = None,
        show_deleted: ShowDeleted = "active",
    ) -> tuple[list[WorkLocation], int]:
        items, total = self._read.get_page(
            page=page,
            page_size=page_size,
            q=q,
            is_active=is_active,
            show_deleted=show_deleted,
        )
        domains = [self._mapper.to_domain(x) for x in items]
        return domains, int(total)

    # -------------------------
    # GET ONE
    # -------------------------
    def get_location(self, location_id: str | ObjectId, *, show_deleted: ShowDeleted = "active") -> WorkLocation:
        raw = self._read.get_by_id(self._oid(location_id), show_deleted=show_deleted)
        if not raw:
            raise WorkLocationNotFoundException(str(location_id))
        return self._mapper.to_domain(raw)

    # -------------------------
    # GET ACTIVE LOCATIONS
    # -------------------------
    def get_active_locations(self) -> list[WorkLocation]:
        """Get all active work locations for check-in validation"""
        items = self._read.get_active_locations()
        return [self._mapper.to_domain(x) for x in items]

    # -------------------------
    # CREATE
    # -------------------------
    def create_location(self, payload, *, created_by_user_id: str | ObjectId) -> WorkLocation:
        actor_oid = self._oid(created_by_user_id)
        
        p = payload.model_dump()
        
        location = self._factory.create_location(payload=p, created_by=actor_oid)
        saved = self._repo.save(self._mapper.to_persistence(location))
        
        return saved

    # -------------------------
    # UPDATE
    # -------------------------
    def update_location(self, location_id: str | ObjectId, payload, *, actor_id: str | ObjectId) -> WorkLocation:
        location = self.get_location(location_id, show_deleted="active")
        
        p = payload.model_dump(exclude_unset=True)
        
        # Update fields
        if "name" in p and p["name"]:
            # Check if new name conflicts with existing
            existing = self._read.get_by_name(p["name"])
            if existing and str(existing["_id"]) != str(location.id):
                raise ValueError(f"Work location with name '{p['name']}' already exists")
            location.name = str(p["name"]).strip()
        
        if "address" in p:
            location.address = str(p["address"]).strip()
        
        if "latitude" in p and "longitude" in p:
            location.update_coordinates(float(p["latitude"]), float(p["longitude"]))
        elif "latitude" in p or "longitude" in p:
            # If only one is provided, use current value for the other
            lat = float(p.get("latitude", location.latitude))
            lon = float(p.get("longitude", location.longitude))
            location.update_coordinates(lat, lon)
        
        if "radius_meters" in p:
            location.update_radius(int(p["radius_meters"]))
        
        if "is_active" in p:
            if p["is_active"]:
                location.activate()
            else:
                location.deactivate()
        
        location.lifecycle.touch(now_utc())
        
        updated = self._repo.update(self._oid(location.id), self._mapper.to_persistence(location))
        if not updated:
            raise WorkLocationNotFoundException(str(location_id))
        
        return updated

    # -------------------------
    # SOFT DELETE
    # -------------------------
    def soft_delete_location(self, location_id: str | ObjectId, *, actor_id: str | ObjectId) -> WorkLocation:
        location = self.get_location(location_id, show_deleted="active")
        
        location.soft_delete(actor_id=actor_id)
        
        updated = self._repo.update(self._oid(location.id), self._mapper.to_persistence(location))
        if not updated:
            raise WorkLocationNotFoundException(str(location_id))
        
        return updated

    # -------------------------
    # RESTORE
    # -------------------------
    def restore_location(self, location_id: str | ObjectId) -> WorkLocation:
        location = self.get_location(location_id, show_deleted="deleted_only")
        
        location.lifecycle.restore()
        
        updated = self._repo.update(self._oid(location.id), self._mapper.to_persistence(location))
        if not updated:
            raise WorkLocationNotFoundException(str(location_id))
        
        return updated
