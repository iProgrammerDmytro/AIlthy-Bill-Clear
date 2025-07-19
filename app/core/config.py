from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_prefix: str = "/api"
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    database_url: str

    project_name: str = "AIlthy BillClear"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
