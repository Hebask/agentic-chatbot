import json
import logging

from sqlalchemy.orm import Session

from app.core.exceptions import ValidationError
from app.services.conversation_service import ConversationService
from app.services.llm_service import LLMService
from app.tools.executor import ToolExecutor

logger = logging.getLogger(__name__)


class AgentService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.llm = LLMService()
        self.tool_executor = ToolExecutor(db)
        self.conversation_service = ConversationService(db)

    def handle_message(self, message: str, conversation_id: int | None = None) -> tuple[str, int]:
        cleaned_message = message.strip()
        if not cleaned_message:
            raise ValidationError("Message cannot be empty")

        logger.info(
            "Agent received message | conversation_id=%s | message=%s",
            conversation_id,
            cleaned_message,
        )

        if conversation_id is None:
            conversation = self.conversation_service.create_conversation(
                title=cleaned_message[:50] or "New Conversation"
            )
            conversation_id = conversation.id
            logger.info("Created new conversation | conversation_id=%s", conversation_id)
        else:
            self.conversation_service.get_conversation(conversation_id)
            logger.info("Using existing conversation | conversation_id=%s", conversation_id)

        self.conversation_service.add_user_message(conversation_id, cleaned_message)

        history = self.conversation_service.list_messages(conversation_id)
        llm_messages = [
            {
                "role": msg.role,
                "content": msg.content,
            }
            for msg in history
        ]

        logger.info(
            "Sending conversation history to LLM | conversation_id=%s | message_count=%s",
            conversation_id,
            len(llm_messages),
        )
        response = self.llm.create_initial_response(llm_messages)

        max_iterations = 5
        for iteration in range(max_iterations):
            function_calls = [
                item
                for item in (getattr(response, "output", []) or [])
                if getattr(item, "type", None) == "function_call"
            ]

            if not function_calls:
                final_reply = self.llm.extract_text(response)
                logger.info(
                    (
                        "Agent produced final reply without further tool calls | "
                        "conversation_id=%s | iteration=%s | reply=%s"
                    ),
                    conversation_id,
                    iteration,
                    final_reply,
                )
                self.conversation_service.add_assistant_message(conversation_id, final_reply)
                return final_reply, conversation_id

            function_call = function_calls[0]
            tool_name = function_call.name
            tool_args_raw = function_call.arguments or "{}"

            logger.info(
                (
                    "LLM requested tool call | conversation_id=%s | "
                    "iteration=%s | tool=%s | raw_arguments=%s"
                ),
                conversation_id,
                iteration,
                tool_name,
                tool_args_raw,
            )

            try:
                tool_args = json.loads(tool_args_raw)
            except json.JSONDecodeError as exc:
                logger.exception(
                    "Failed to decode tool arguments | tool=%s | raw_arguments=%s",
                    tool_name,
                    tool_args_raw,
                )
                raise ValidationError(f"Invalid tool arguments returned by model: {exc}") from exc

            tool_result = self.tool_executor.execute(tool_name, tool_args)

            logger.info(
                (
                    "Tool executed successfully | conversation_id=%s | "
                    "iteration=%s | tool=%s | result=%s"
                ),
                conversation_id,
                iteration,
                tool_name,
                tool_result,
            )

            response = self.llm.continue_with_tool_output(
                previous_response_id=response.id,
                tool_call_id=function_call.call_id,
                tool_output=json.dumps(tool_result),
            )

        final_reply = "The agent stopped after reaching the maximum tool-iteration limit."
        logger.warning(
            "Agent hit max iterations | conversation_id=%s | max_iterations=%s",
            conversation_id,
            max_iterations,
        )
        self.conversation_service.add_assistant_message(conversation_id, final_reply)
        return final_reply, conversation_id
