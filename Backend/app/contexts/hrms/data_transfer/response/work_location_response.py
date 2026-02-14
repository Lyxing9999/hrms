# app/contexts/hrms/data_transfer/response/work_location_response.py
from typing import Optional
from pydantic import BaseModel, ConfigDict

from app.contexts.shared.lifecycle.dto import LifecycleDTO
from app.contexts.admin.data_transfer.responses.common import PaginatedDTO


class WorkLocationDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore", populate_by_name=True)

    id: str
    name: str
    address: str
    latitude: float
    longitude: float
    radius_meters: int
    is_active: bool
    created_by: Optional[str] = None
    lifecycle: LifecycleDTO


class WorkLocationPaginatedDTO(PaginatedDTO[WorkLocationDTO]):
    pass
