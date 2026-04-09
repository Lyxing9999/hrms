from __future__ import annotations

from pydantic import BaseModel, Field


class DeductionRuleCreateSchema(BaseModel):
    type: str = Field(..., min_length=1, max_length=50)
    min_minutes: int = Field(..., ge=0)
    max_minutes: int | None = Field(default=None, ge=0)
    deduction_percentage: float = Field(..., ge=0, le=100)
    is_active: bool = True


class DeductionRuleUpdateSchema(BaseModel):
    min_minutes: int | None = Field(default=None, ge=0)
    max_minutes: int | None = Field(default=None, ge=0)
    deduction_percentage: float | None = Field(default=None, ge=0, le=100)
    is_active: bool | None = None