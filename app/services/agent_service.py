import json
from sqlalchemy.orm import Session

from app.services.llm_service import LLMService
from app.tools.executor import ToolExecutor


class AgentService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.llm = LLMService()
        self.tool_executor = ToolExecutor(db)

    def handle_message(self, message: str) -> str:
        response = self.llm.create_initial_response(message)

        max_iterations = 5
        for _ in range(max_iterations):
            function_calls = [
                item
                for item in (getattr(response, "output", []) or [])
                if getattr(item, "type", None) == "function_call"
            ]

            if not function_calls:
                return self.llm.extract_text(response)

            # For v1, handle one tool call at a time.
            function_call = function_calls[0]
            tool_name = function_call.name
            tool_args_raw = function_call.arguments or "{}"
            tool_args = json.loads(tool_args_raw)

            tool_result = self.tool_executor.execute(tool_name, tool_args)

            response = self.llm.continue_with_tool_output(
                previous_response_id=response.id,
                tool_call_id=function_call.call_id,
                tool_output=json.dumps(tool_result),
            )

        return "The agent stopped after reaching the maximum tool-iteration limit."