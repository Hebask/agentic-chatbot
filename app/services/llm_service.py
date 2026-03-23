from openai import OpenAI

from app.core.config import settings
from app.tools.definitions import TOOLS


class LLMService:
    def __init__(self) -> None:
        self.client = OpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url,
        )
        self.model = settings.openai_model

    def create_initial_response(self, user_message: str):
        return self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": settings.agent_system_prompt,
                },
                {
                    "role": "user",
                    "content": user_message,
                },
            ],
            tools=TOOLS,
        )

    def continue_with_tool_output(
        self,
        previous_response_id: str,
        tool_call_id: str,
        tool_output: str,
    ):
        return self.client.responses.create(
            model=self.model,
            previous_response_id=previous_response_id,
            input=[
                {
                    "type": "function_call_output",
                    "call_id": tool_call_id,
                    "output": tool_output,
                }
            ],
            tools=TOOLS,
        )

    @staticmethod
    def extract_text(response) -> str:
        output_text = getattr(response, "output_text", None)
        if output_text:
            return output_text.strip()

        fragments: list[str] = []
        for item in getattr(response, "output", []) or []:
            if getattr(item, "type", None) == "message":
                for content in getattr(item, "content", []) or []:
                    text_value = getattr(content, "text", None)
                    if text_value:
                        fragments.append(text_value)

        return "\n".join(fragments).strip() or "I could not generate a response."