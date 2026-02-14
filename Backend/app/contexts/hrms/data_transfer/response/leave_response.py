from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import date

from app.contexts.shared.lifecycle.dto import LifecycleDTO
from app.contexts.admin.data_transfer.responses.common import PaginatedDTO


class LeaveDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore", populate_by_name=True)

    id: str
    employee_id: str
    leave_type: str
    start_date: date
    end_date: date
    reason: str
    
    contract_start: date
    contract_end: date
    is_paid: bool
    
    status: str
    manager_user_id: Optional[str] = None
    manager_comment: Optional[str] = None
    
    lifecycle: LifecycleDTO


class LeavePaginatedDTO(PaginatedDTO[LeaveDTO]):
    pass
