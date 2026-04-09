# app/contexts/hrms/read_models/public_holiday_read_model.py
from typing import Tuple, List, Dict, Any
from datetime import date as date_type
from bson import ObjectId
from pymongo.database import Database
from app.contexts.shared.lifecycle.filters import by_show_deleted, ShowDeleted
from app.contexts.shared.model_converter import mongo_converter


class PublicHolidayReadModel:
    def __init__(self, db: Database):
        self.collection = db["hr_public_holidays"]

    def get_by_id(self, holiday_id: ObjectId | str, *, show_deleted: ShowDeleted = "active") -> dict | None:
        oid = mongo_converter.convert_to_object_id(holiday_id)
        if not oid:
            return None
        return self.collection.find_one(by_show_deleted(show_deleted, {"_id": oid}))

    def get_by_date(self, date: date_type, *, show_deleted: ShowDeleted = "active") -> dict | None:
        """Check if a holiday exists on a specific date"""
        date_str = date.isoformat() if isinstance(date, date_type) else date
        return self.collection.find_one(by_show_deleted(show_deleted, {"date": date_str}))

    def get_holidays_in_range(self, start_date: date_type, end_date: date_type, *, show_deleted: ShowDeleted = "active") -> List[dict]:
        """Get all holidays within a date range"""
        start_str = start_date.isoformat()
        end_str = end_date.isoformat()
        
        query = by_show_deleted(show_deleted, {
            "date": {"$gte": start_str, "$lte": end_str}
        })
        
        return list(self.collection.find(query).sort("date", 1))

    def get_holidays_by_year(self, year: int, *, show_deleted: ShowDeleted = "active") -> List[dict]:
        """Get all holidays for a specific year"""
        start_date = date_type(year, 1, 1)
        end_date = date_type(year, 12, 31)
        return self.get_holidays_in_range(start_date, end_date, show_deleted=show_deleted)

    def get_page(
        self,
        *,
        page: int = 1,
        page_size: int = 10,
        q: str | None = None,
        year: int | None = None,
        show_deleted: ShowDeleted = "active",
    ) -> Tuple[List[Dict[str, Any]], int]:
        page = max(1, int(page))
        page_size = min(max(1, int(page_size)), 100)
        skip = (page - 1) * page_size

        base: Dict[str, Any] = {}
        
        if q and (s := q.strip()):
            base["$or"] = [
                {"name": {"$regex": s, "$options": "i"}},
                {"name_kh": {"$regex": s, "$options": "i"}},
                {"description": {"$regex": s, "$options": "i"}},
            ]
        
        if year:
            start_date = date_type(year, 1, 1).isoformat()
            end_date = date_type(year, 12, 31).isoformat()
            base["date"] = {"$gte": start_date, "$lte": end_date}

        query = by_show_deleted(show_deleted, base)
        total = self.collection.count_documents(query)

        items = list(
            self.collection.find(query)
            .sort("date", 1)  # Sort by date ascending
            .skip(skip)
            .limit(page_size)
        )
        return items, total
