from __future__ import annotations

from datetime import date as date_type
from pydantic import BaseModel, Field, model_validator


class PublicHolidayCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    name_kh: str | None = Field(default=None, max_length=150)
    date: date_type
    is_paid: bool = True
    description: str | None = Field(default=None, max_length=500)

    @model_validator(mode="after")
    def normalize_fields(self):
        self.name = self.name.strip()
        if self.name_kh is not None:
            self.name_kh = self.name_kh.strip() or None
        if self.description is not None:
            self.description = self.description.strip() or None
        return self


class PublicHolidayUpdateSchema(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    name_kh: str | None = Field(default=None, max_length=150)
    date: date_type | None = None
    is_paid: bool | None = None
    description: str | None = Field(default=None, max_length=500)

    @model_validator(mode="after")
    def normalize_fields(self):
        if self.name is not None:
            self.name = self.name.strip()
        if self.name_kh is not None:
            self.name_kh = self.name_kh.strip() or None
        if self.description is not None:
            self.description = self.description.strip() or None
        return self
    



class PublicHolidayImportDefaultsSchema(BaseModel):
    year: int = Field(..., ge=2000, le=2100)