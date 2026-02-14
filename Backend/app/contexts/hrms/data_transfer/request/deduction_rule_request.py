# app/contexts/hrms/data_transfer/request/deduction_rule_request.py
from pydantic import BaseModel, Field, field_validator


class DeductionRuleCreateSchema(BaseModel):
    type: str = Field(..., description="Deduction type: late, absent, early_leave")
    min_minutes: int = Field(..., ge=0, description="Minimum minutes")
    max_minutes: int = Field(..., ge=0, description="Maximum minutes")
    deduction_percentage: float = Field(..., ge=0, le=100, description="Deduction percentage (0-100)")
    is_active: bool = Field(default=True, description="Rule is active")
    
    @field_validator("type")
    @classmethod
    def validate_type(cls, v):
        allowed = ["late", "absent", "early_leave"]
        if v.lower() not in allowed:
            raise ValueError(f"Type must be one of: {', '.join(allowed)}")
        return v.lower()
    
    @field_validator("max_minutes")
    @classmethod
    def validate_range(cls, v, info):
        if "min_minutes" in info.data and v < info.data["min_minutes"]:
            raise ValueError("max_minutes must be >= min_minutes")
        return v


class DeductionRuleUpdateSchema(BaseModel):
    type: str | None = None
    min_minutes: int | None = Field(None, ge=0)
    max_minutes: int | None = Field(None, ge=0)
    deduction_percentage: float | None = Field(None, ge=0, le=100)
    is_active: bool | None = None
    
    @field_validator("type")
    @classmethod
    def validate_type(cls, v):
        if v is not None:
            allowed = ["late", "absent", "early_leave"]
            if v.lower() not in allowed:
                raise ValueError(f"Type must be one of: {', '.join(allowed)}")
            return v.lower()
        return v
