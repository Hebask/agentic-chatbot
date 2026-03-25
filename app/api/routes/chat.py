from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.exceptions import NotFoundError, ValidationError
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    ConversationCreateResponse,
    ConversationListResponse,
    ConversationMessagesResponse,
    ConversationSummaryResponse,
    MessageResponse,
)
from app.services.agent_service import AgentService
from app.services.conversation_service import ConversationService

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def chat(payload: ChatRequest, db: Session = Depends(get_db)) -> ChatResponse:
    try:
        agent = AgentService(db)
        reply, conversation_id = agent.handle_message(
            message=payload.message,
            conversation_id=payload.conversation_id,
        )
        return ChatResponse(reply=reply, conversation_id=conversation_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {exc}") from exc


@router.post("/conversations", response_model=ConversationCreateResponse)
def create_conversation(db: Session = Depends(get_db)) -> ConversationCreateResponse:
    service = ConversationService(db)
    conversation = service.create_conversation(title="New Conversation")
    return ConversationCreateResponse(conversation_id=conversation.id)


@router.get("/conversations", response_model=ConversationListResponse)
def list_conversations(db: Session = Depends(get_db)) -> ConversationListResponse:
    service = ConversationService(db)
    conversations = service.list_conversations()
    return ConversationListResponse(
        conversations=[
            ConversationSummaryResponse.model_validate(conversation)
            for conversation in conversations
        ]
    )


@router.get("/conversations/{conversation_id}", response_model=ConversationMessagesResponse)
def get_conversation_messages(
    conversation_id: int,
    db: Session = Depends(get_db),
) -> ConversationMessagesResponse:
    try:
        service = ConversationService(db)
        messages = service.list_messages(conversation_id)
        return ConversationMessagesResponse(
            conversation_id=conversation_id,
            messages=[MessageResponse.model_validate(msg) for msg in messages],
        )
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
