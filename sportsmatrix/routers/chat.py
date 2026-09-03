"""
FastAPI Router for Pydantic AI Chatbot LLM Service (/api/v1/chat)
"""

from fastapi import APIRouter, HTTPException
from sportsmatrix.chatbot.schemas import ChatRequest, ChatResponse
from sportsmatrix.chatbot.agent import process_sports_chat

router = APIRouter(prefix="/api/v1/chat", tags=["Pydantic AI Chatbot"])


@router.post("", response_model=ChatResponse)
def sportsmatrix_chatbot(req: ChatRequest):
    """
    Unified Pydantic AI Chatbot LLM Endpoint.
    Receives user queries about any sports prediction service (MLB, Basketball, NFL, CFB),
    invokes tool functions to query backend engines, and returns a data-backed LLM response.
    """
    try:
        return process_sports_chat(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
