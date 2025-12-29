from pydantic import BaseModel, Field
from typing import List, Optional


class AdvisoryInput(BaseModel):
    task_description: str = Field(..., min_length=1)
    available_tools: List[str] = Field(default_factory=list)

    domain: Optional[str] = None
    urgency: Optional[str] = None  # low | medium | high
    constraints: Optional[List[str]] = None
