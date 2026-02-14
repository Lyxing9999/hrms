from pydantic import BaseModel, Field

class PayrollGenerateSchema(BaseModel):
    month: str = Field(..., pattern=r"^\d{4}-\d{2}$", description="YYYY-MM")