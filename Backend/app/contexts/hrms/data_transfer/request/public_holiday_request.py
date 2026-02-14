# app/contexts/hrms/data_transfer/request/public_holiday_request.py
from pydantic import BaseModel, Field
from datetime import date as date_type


class PublicHolidayCreateSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=200, description="Holiday name")
    name_kh: str | None = Field(None, max_length=200, description="Khmer name")
    date: date_type = Field(..., description="Holiday date")
    is_paid: bool = Field(default=True, description="Is this a paid holiday")
    description: str | None = Field(None, max_length=500, description="Holiday description")


class PublicHolidayUpdateSchema(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=200)
    name_kh: str | None = Field(None, max_length=200)
    date: date_type | None = None
    is_paid: bool | None = None
    description: str | None = Field(None, max_length=500)
