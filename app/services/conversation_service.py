from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.db.models import Conversation, Message
from app.repositories.conversation_repository import ConversationRepository


class ConversationService:
    def __init__(self, db: Session) -> None:
        self.repo = ConversationRepository(db)

    def create_conversation(self, title: str | None = None) -> Conversation:
        return self.repo.create_conversation(title=title)

    def get_conversation(self, conversation_id: int) -> Conversation:
        conversation = self.repo.get_conversation(conversation_id)
        if not conversation:
            raise NotFoundError(f"Conversation with id {conversation_id} not found")
        return conversation

    def list_conversations(self) -> list[Conversation]:
        return self.repo.list_conversations()

    def add_user_message(self, conversation_id: int, content: str) -> Message:
        return self.repo.add_message(conversation_id, "user", content)

    def add_assistant_message(self, conversation_id: int, content: str) -> Message:
        return self.repo.add_message(conversation_id, "assistant", content)

    def list_messages(self, conversation_id: int) -> list[Message]:
        self.get_conversation(conversation_id)
        return self.repo.list_messages(conversation_id)