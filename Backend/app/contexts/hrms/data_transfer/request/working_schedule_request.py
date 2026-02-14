# app/contexts/hrms/data_transfer/request/working_schedule_request.py
from pydantic import BaseModel, Field, field_validator
from datetime import time as time_type


class WorkingScheduleCreateSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Schedule name")
    start_time: time_type = Field(..., description="Working start time (HH:MM)")
    end_time: time_type = Field(..., description="Working end time (HH:MM)")
    working_days: list[int] = Field(..., description="Working days (0=Monday, 6=Sunday)")
    is_default: bool = Field(default=False, description="Set as default schedule")
    
    @field_validator("working_days")
    @classmethod
    def validate_working_days(cls, v):
        if not v or not all(0 <= day <= 6 for day in v):
            raise ValueError("Working days must be between 0 (Monday) and 6 (Sunday)")
        return sorted(set(v))
    
    @field_validator("end_time")
    @classmethod
    def validate_time_range(cls, v, info):
        if "start_time" in info.data and v <= info.data["start_time"]:
            raise ValueError("End time must be after start time")
        return v


class WorkingScheduleUpdateSchema(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100)
    start_time: time_type | None = None
    end_time: time_type | None = None
    working_days: list[int] | None = None
    is_default: bool | None = None
    
    @field_validator("working_days")
    @classmethod
    def validate_working_days(cls, v):
        if v is not None and (not v or not all(0 <= day <= 6 for day in v)):
            raise ValueError("Working days must be between 0 (Monday) and 6 (Sunday)")
        return sorted(set(v)) if v else None
