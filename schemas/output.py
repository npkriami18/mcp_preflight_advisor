from pydantic import BaseModel, Field
from typing import List, Optional


class ToolSuggestion(BaseModel):
    tool_name: str
    confidence: float = Field(ge=0.0, le=1.0)
    rationale: str


class AdvisoryWarning(BaseModel):
    code: str
    message: str
    severity: str  # info | caution | high


class AdvisoryResponse(BaseModel):
    suggested_sequence: List[ToolSuggestion]
    overall_confidence: float = Field(ge=0.0, le=1.0)
    warnings: List[AdvisoryWarning]
    explanation: str
    evidence_summary: Optional[str] = None
