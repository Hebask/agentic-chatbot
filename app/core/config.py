from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Agentic Chatbot"
    app_env: str = "development"
    app_debug: bool = True
    app_host: str = "127.0.0.1"
    app_port: int = 8000

    database_url: str = "sqlite:///./agentic_chatbot.db"

    openai_api_key: str = ""
    openai_model: str = "gpt-5.4"
    openai_base_url: str = "https://api.openai.com/v1"

    agent_system_prompt: str = (
        "You are an agentic productivity assistant. "
        "You help users manage tasks and notes. "
        "Use tools whenever the user asks to create, update, store, search, or list data. "
        "Do not invent task IDs or note contents. "
        "When a tool is needed, call the appropriate tool. "
        "When no tool is needed, answer directly and clearly."
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
