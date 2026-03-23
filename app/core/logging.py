from datetime import datetime
from pydantic import BaseModel, Field
import logging
import sys


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    conversation_id: int | None = None


class ChatResponse(BaseModel):
    reply: str
    conversation_id: int


class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ConversationCreateResponse(BaseModel):
    conversation_id: int


class ConversationMessagesResponse(BaseModel):
    conversation_id: int
    messages: list[MessageResponse]

def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )