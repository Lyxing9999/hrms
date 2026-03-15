from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class PublicHolidayCreateSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    name_kh: Optional[str] = None
    date: date
    is_paid: bool = True
    description: Optional[str] = None


class PublicHolidayUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=120)
    name_kh: Optional[str] = None
    date: Optional[date] = None
    is_paid: Optional[bool] = None
    description: Optional[str] = None