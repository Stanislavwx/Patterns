from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    app_name: str = "Smart Day Planner"
    environment: str = "development"
    openweather_api_key: str = "change-me"
    default_city: str = "Kyiv"
    weather_poll_interval: int = 1800
    mongodb_uri: str = "mongodb://mongo:27017"
    mongodb_db: str = "smart_planner"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_prefix="", env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
