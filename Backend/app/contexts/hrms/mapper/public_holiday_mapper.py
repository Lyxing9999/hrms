from __future__ import annotations

from datetime import date as date_type, datetime
from bson import ObjectId

from app.contexts.hrms.domain.public_holiday import PublicHoliday
from app.contexts.hrms.data_transfer.response.public_holiday_response import PublicHolidayDTO
from app.contexts.shared.lifecycle.domain import Lifecycle
from app.contexts.shared.lifecycle.dto import LifecycleDTO
from app.contexts.shared.model_converter import mongo_converter


class PublicHolidayMapper:
    @staticmethod
    def _oid(v) -> ObjectId | None:
        return mongo_converter.convert_to_object_id(v)

    @staticmethod
    def _sid(v) -> str | None:
        if v is None:
            return None
        return str(v)

    @staticmethod
    def _parse_date(v):
        if v is None:
            return None
        if isinstance(v, date_type):
            return v
        if isinstance(v, datetime):
            return v.date()
        if isinstance(v, str):
            return date_type.fromisoformat(v)
        return v

    @staticmethod
    def to_domain(data: dict) -> PublicHoliday:
        if not isinstance(data, dict):
            raise TypeError(f"to_domain expected dict, got {type(data)}")

        lc_src = data.get("lifecycle") or {}
        lifecycle = Lifecycle(
            created_at=lc_src.get("created_at") or data.get("created_at"),
            updated_at=lc_src.get("updated_at") or data.get("updated_at"),
            deleted_at=lc_src.get("deleted_at") or data.get("deleted_at"),
            deleted_by=lc_src.get("deleted_by") or data.get("deleted_by"),
        )

        return PublicHoliday(
            id=PublicHolidayMapper._oid(data.get("_id") or data.get("id")),
            name=data.get("name", ""),
            name_kh=data.get("name_kh"),
            date=PublicHolidayMapper._parse_date(data.get("date")),
            is_paid=bool(data.get("is_paid", True)),
            description=data.get("description"),
            created_by=PublicHolidayMapper._oid(data.get("created_by")),
            lifecycle=lifecycle,
        )

    @staticmethod
    def to_persistence(holiday: PublicHoliday) -> dict:
        if not isinstance(holiday, PublicHoliday):
            raise TypeError(f"to_persistence expected PublicHoliday, got {type(holiday)}")

        lc = holiday.lifecycle
        doc = {
            "name": holiday.name,
            "name_kh": holiday.name_kh,
            "date": holiday.date.isoformat() if holiday.date else None,
            "is_paid": holiday.is_paid,
            "description": holiday.description,
            "created_by": PublicHolidayMapper._oid(holiday.created_by),
            "lifecycle": {
                "created_at": lc.created_at,
                "updated_at": lc.updated_at,
                "deleted_at": lc.deleted_at,
                "deleted_by": PublicHolidayMapper._oid(lc.deleted_by),
            },
        }

        if holiday.id:
            doc["_id"] = PublicHolidayMapper._oid(holiday.id)

        return doc

    @staticmethod
    def to_dto(holiday: PublicHoliday) -> PublicHolidayDTO:
        lc = holiday.lifecycle
        return PublicHolidayDTO(
            id=str(holiday.id),
            name=holiday.name,
            name_kh=holiday.name_kh,
            date=holiday.date,
            is_paid=holiday.is_paid,
            description=holiday.description,
            created_by=PublicHolidayMapper._sid(holiday.created_by),
            lifecycle=LifecycleDTO(
                created_at=lc.created_at,
                updated_at=lc.updated_at,
                deleted_at=lc.deleted_at,
                deleted_by=PublicHolidayMapper._sid(lc.deleted_by),
            ),
        )