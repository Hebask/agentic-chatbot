from openai import OpenAI

from app.core.config import get_settings

settings = get_settings()


class LLMService:
    def __init__(self) -> None:
        self.client = OpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url,
        )
        self.model = settings.openai_model
        self.system_prompt = settings.agent_system_prompt

    def create_initial_response(self, messages: list[dict]):
        input_messages = [{"role": "system", "content": self.system_prompt}, *messages]

        return self.client.responses.create(
            model=self.model,
            input=input_messages,
            tools=[],
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
            tools=[],
        )

    @staticmethod
    def extract_text(response) -> str:
        return getattr(response, "output_text", "").strip()