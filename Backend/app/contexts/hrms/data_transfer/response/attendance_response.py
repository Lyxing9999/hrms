from pydantic import BaseModel, Field
from datetime import datetime
from app.contexts.shared.lifecycle.dto import LifecycleDTO


class AttendanceDTO(BaseModel):
    id: str
    employee_id: str
    check_in_time: datetime
    check_out_time: datetime | None = None
    location_id: str | None = None
    check_in_latitude: float | None = None
    check_in_longitude: float | None = None
    check_out_latitude: float | None = None
    check_out_longitude: float | None = None
    status: str
    notes: str | None = None
    late_minutes: int = 0
    early_leave_minutes: int = 0
    lifecycle: LifecycleDTO

    class Config:
        from_attributes = True


class AttendancePaginatedDTO(BaseModel):
    items: list[AttendanceDTO]
    total: int
    page: int
    page_size: int
    total_pages: int


class AttendanceStatsDTO(BaseModel):
    total_days: int
    present_days: int
    late_days: int
    early_leave_days: int
    total_late_minutes: int
    total_early_leave_minutes: int
    attendance_rate: float = Field(description="Percentage of present days")
