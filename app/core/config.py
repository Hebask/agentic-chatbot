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

    jwt_secret_key: str = "change_this_to_a_long_random_secret"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60

    agent_system_prompt: str = (
        "You are an agentic assistant. "
        "When useful, call tools to help the user complete actions. "
        "Be concise, accurate, and action-oriented."
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