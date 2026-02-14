# app/contexts/hrms/data_transfer/request/work_location_request.py
from pydantic import BaseModel, Field, field_validator


class WorkLocationCreateSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Location name")
    address: str = Field(..., min_length=5, max_length=500, description="Full address")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude coordinate")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude coordinate")
    radius_meters: int = Field(..., ge=10, le=1000, description="Acceptable radius in meters")
    is_active: bool = Field(default=True, description="Location is active")


class WorkLocationUpdateSchema(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100)
    address: str | None = Field(None, min_length=5, max_length=500)
    latitude: float | None = Field(None, ge=-90, le=90)
    longitude: float | None = Field(None, ge=-180, le=180)
    radius_meters: int | None = Field(None, ge=10, le=1000)
    is_active: bool | None = None
