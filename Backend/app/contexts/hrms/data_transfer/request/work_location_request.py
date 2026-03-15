from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class WorkLocationCreateSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    address: str = Field(..., min_length=2, max_length=255)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    radius_meters: int = Field(..., ge=10, le=1000)
    is_active: bool = True


class WorkLocationUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=120)
    address: Optional[str] = Field(None, min_length=2, max_length=255)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    radius_meters: Optional[int] = Field(None, ge=10, le=1000)
    is_active: Optional[bool] = None