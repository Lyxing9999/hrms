# app/contexts/hrms/data_transfer/response/public_holiday_response.py
from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import date

from app.contexts.shared.lifecycle.dto import LifecycleDTO
from app.contexts.admin.data_transfer.responses.common import PaginatedDTO


class PublicHolidayDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore", populate_by_name=True)

    id: str
    name: str
    name_kh: Optional[str] = None
    date: date
    is_paid: bool
    description: Optional[str] = None
    created_by: Optional[str] = None
    lifecycle: LifecycleDTO


class PublicHolidayPaginatedDTO(PaginatedDTO[PublicHolidayDTO]):
    pass
