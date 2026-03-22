from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field, model_validator


class AttendanceCheckInSchema(BaseModel):
    check_in_time: datetime
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    wrong_location_reason: str | None = Field(default=None, max_length=300)

    @model_validator(mode="after")
    def normalize_reason(self):
        if self.wrong_location_reason is not None:
            self.wrong_location_reason = self.wrong_location_reason.strip() or None
        return self


class AttendanceCheckOutSchema(BaseModel):
    check_out_time: datetime
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)


class AttendanceApproveWrongLocationSchema(BaseModel):
    approved: bool
    comment: str | None = Field(default=None, max_length=300)

    @model_validator(mode="after")
    def normalize_comment(self):
        if self.comment is not None:
            self.comment = self.comment.strip() or None
        return self