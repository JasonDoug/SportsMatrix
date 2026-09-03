"""
Pydantic schemas for the SportsMatrix Pydantic AI Chatbot LLM service.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class ChatRequest(BaseModel):
    prompt: str = Field(
        ...,
        description="User query about any sports prediction service (MLB, Basketball, NFL, CFB)",
        json_schema_extra={"example": "Who is favored in the Chiefs vs 49ers NFL matchup?"}
    )
    model: Optional[str] = Field(
        None,
        description="Optional model identifier for Pydantic AI (e.g. 'openai:gpt-4o', 'gemini:gemini-1.5-flash', or default auto-detect)",
        json_schema_extra={"example": "auto"}
    )
    conversation_id: Optional[str] = Field(
        None,
        description="Optional conversation state tracking ID"
    )


class ToolCallLog(BaseModel):
    tool_name: str
    args: Dict[str, Any]
    summary: str


class ChatResponse(BaseModel):
    response: str
    conversation_id: Optional[str] = None
    tools_used: List[ToolCallLog] = []
    service_sources: List[str] = []
