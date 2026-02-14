from bson import ObjectId
from datetime import date as date_type, datetime, time as time_type
from typing import Any

from app.contexts.hrms.domain.employee import Employee
from app.contexts.shared.lifecycle.domain import Lifecycle
from app.contexts.shared.model_converter import mongo_converter


class EmployeeMapper:
    @staticmethod
    def _sid(v) -> str | None:
        if v is None:
            return None
        return str(v)

    @staticmethod
    def _oid(v) -> ObjectId | None:
        return mongo_converter.convert_to_object_id(v)

    # ---- NEW: normalize to_domains for Mongo ----
    @staticmethod
    def _mongo_safe(v: Any) -> Any:
        """
        Convert values Mongo can't encode:
          - date -> "YYYY-MM-DD"
          - time -> "HH:MM:SS"
        Keep datetime as-is (Mongo can store it).
        Works recursively for dict/list.
        """
        if v is None:
            return None

        if isinstance(v, datetime):
            return v  # OK for Mongo

        if isinstance(v, date_type):
            return v.isoformat()  # "2026-02-11"

        if isinstance(v, time_type):
            return v.strftime("%H:%M:%S")

        if isinstance(v, dict):
            return {k: EmployeeMapper._mongo_safe(val) for k, val in v.items()}

        if isinstance(v, list):
            return [EmployeeMapper._mongo_safe(x) for x in v]

        return v

    @staticmethod
    def to_domain(data: dict) -> Employee:
        if not isinstance(data, dict):
            raise TypeError(f"to_domain expected dict, got {type(data)}")
        lc_src = data.get("lifecycle") or {}
        lifecycle = Lifecycle(
            created_at=lc_src.get("created_at") or data.get("created_at"),
            updated_at=lc_src.get("updated_at") or data.get("updated_at"),
            deleted_at=lc_src.get("deleted_at") or data.get("deleted_at"),
            deleted_by=lc_src.get("deleted_by") or data.get("deleted_by"),
        )

        return Employee(
            id=EmployeeMapper._sid(data.get("_id") or data.get("id")),
            user_id=EmployeeMapper._sid(data.get("user_id")),
            employee_code=data.get("employee_code") or "",
            full_name=data.get("full_name") or "",
            department=data.get("department"),
            position=data.get("position"),
            employment_type=data.get("employment_type") or "contract",
            contract=data.get("contract"),
            manager_user_id=EmployeeMapper._sid(data.get("manager_user_id")),
            schedule_id=EmployeeMapper._sid(data.get("schedule_id")),
            status=data.get("status") or "active",
            created_by=EmployeeMapper._sid(data.get("created_by")),
            photo_url=data.get("photo_url"),
            lifecycle=lifecycle,
        )

    @staticmethod
    def to_persistence(emp: Employee) -> dict:
        if not isinstance(emp, Employee):
            raise TypeError(f"to_persistence expected Employee, got {type(emp)}")
        lc = emp.lifecycle
        doc = {
            "user_id": EmployeeMapper._oid(emp.user_id),
            "employee_code": emp.employee_code,
            "full_name": emp.full_name,
            "department": emp.department,
            "position": emp.position,
            "employment_type": (
                emp.employment_type.value
                if hasattr(emp.employment_type, "value")
                else str(emp.employment_type)
            ),
            "contract": EmployeeMapper._mongo_safe(emp.contract),
            "manager_user_id": EmployeeMapper._oid(emp.manager_user_id),
            "schedule_id": EmployeeMapper._oid(emp.schedule_id),
            "status": emp.status,
            "created_by": EmployeeMapper._oid(emp.created_by),
            "photo_url": emp.photo_url,
            "lifecycle": {
                "created_at": lc.created_at,
                "updated_at": lc.updated_at,
                "deleted_at": lc.deleted_at,
                "deleted_by": EmployeeMapper._oid(lc.deleted_by),  # ✅ convert if string
            },
        }

        # only include _id if it's present AND valid (usually for insert)
        if emp.id:
            doc["_id"] = EmployeeMapper._oid(emp.id)

        return doc