from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field, model_validator


class DeductionRuleCreateSchema(BaseModel):
    type: str
    min_minutes: int = Field(..., ge=0)
    max_minutes: Optional[int] = Field(None, ge=0)
    deduction_percentage: float = Field(..., ge=0, le=100)
    is_active: bool = True

    @model_validator(mode="after")
    def validate_range(self):
        if self.max_minutes is not None and self.max_minutes < self.min_minutes:
            raise ValueError("max_minutes cannot be less than min_minutes")
        return self


class DeductionRuleUpdateSchema(BaseModel):
    type: Optional[str] = None
    min_minutes: Optional[int] = Field(None, ge=0)
    max_minutes: Optional[int] = Field(None, ge=0)
    deduction_percentage: Optional[float] = Field(None, ge=0, le=100)
    is_active: Optional[bool] = None