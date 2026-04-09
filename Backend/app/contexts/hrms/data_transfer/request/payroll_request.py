from __future__ import annotations

from pydantic import BaseModel, Field


class GeneratePayrollSchema(BaseModel):
    month: str = Field(..., min_length=7, max_length=7)  # YYYY-MM


class FinalizePayrollRunSchema(BaseModel):
    comment: str | None = Field(default=None, max_length=500)


class MarkPayrollRunPaidSchema(BaseModel):
    comment: str | None = Field(default=None, max_length=500)