from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class AdvisoryInput(BaseModel):
    task_description: str = Field(..., min_length=1)
    mcp_tool_catalog: Dict[str, str] = Field(description="Complete set of MCP tools with their descriptions available via the MCP client. Not filtered or task-selected.")
    suggestions_count: Optional[int] = Field(5, ge=1, le=20, description="Number of tool suggestions to provide.")
    domain: Optional[str] = None
    urgency: Optional[str] = None  # low | medium | high
    constraints: Optional[List[str]] = None
