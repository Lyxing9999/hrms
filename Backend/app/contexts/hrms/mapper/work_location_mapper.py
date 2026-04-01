from __future__ import annotations

from bson import ObjectId

from app.contexts.hrms.domain.work_location import WorkLocation
from app.contexts.shared.lifecycle.domain import Lifecycle
from app.contexts.shared.lifecycle.dto import LifecycleDTO
from app.contexts.hrms.data_transfer.response.work_location_response import WorkLocationDTO
from app.contexts.shared.model_converter import mongo_converter


class WorkLocationMapper:
    @staticmethod
    def _oid(v) -> ObjectId | None:
        return mongo_converter.convert_to_object_id(v)

    @staticmethod
    def _sid(v) -> str | None:
        if v is None:
            return None
        return str(v)

    @staticmethod
    def to_domain(data: dict) -> WorkLocation:
        if not isinstance(data, dict):
            raise TypeError(f"to_domain expected dict, got {type(data)}")

        lc_src = data.get("lifecycle") or {}
        lifecycle = Lifecycle(
            created_at=lc_src.get("created_at") or data.get("created_at"),
            updated_at=lc_src.get("updated_at") or data.get("updated_at"),
            deleted_at=lc_src.get("deleted_at") or data.get("deleted_at"),
            deleted_by=WorkLocationMapper._oid(
                lc_src.get("deleted_by") or data.get("deleted_by")
            ),
        )

        return WorkLocation(
            id=WorkLocationMapper._oid(data.get("_id") or data.get("id")),
            name=data.get("name") or "",
            address=data.get("address") or "",
            latitude=float(data.get("latitude", 0)),
            longitude=float(data.get("longitude", 0)),
            radius_meters=int(data.get("radius_meters", 0)),
            is_active=bool(data.get("is_active", True)),
            created_by=WorkLocationMapper._oid(data.get("created_by")),
            lifecycle=lifecycle,
        )

    @staticmethod
    def to_persistence(location: WorkLocation) -> dict:
        if not isinstance(location, WorkLocation):
            raise TypeError(f"to_persistence expected WorkLocation, got {type(location)}")

        lc = location.lifecycle
        doc = {
            "name": location.name,
            "address": location.address,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "radius_meters": location.radius_meters,
            "is_active": location.is_active,
            "created_by": WorkLocationMapper._oid(location.created_by),
            "lifecycle": {
                "created_at": lc.created_at,
                "updated_at": lc.updated_at,
                "deleted_at": lc.deleted_at,
                "deleted_by": WorkLocationMapper._oid(lc.deleted_by),
            },
        }

        if location.id:
            doc["_id"] = WorkLocationMapper._oid(location.id)

        return doc

    @staticmethod
    def to_dto(location: WorkLocation) -> WorkLocationDTO:
        lc = location.lifecycle
        return WorkLocationDTO(
            id=WorkLocationMapper._sid(location.id),
            name=location.name,
            address=location.address,
            latitude=location.latitude,
            longitude=location.longitude,
            radius_meters=location.radius_meters,
            is_active=location.is_active,
            created_by=WorkLocationMapper._sid(location.created_by),
            lifecycle=LifecycleDTO(
                created_at=lc.created_at,
                updated_at=lc.updated_at,
                deleted_at=lc.deleted_at,
                deleted_by=WorkLocationMapper._sid(lc.deleted_by),
            ),
        )