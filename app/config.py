"""Configuration settings for the VoteApp application."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    DATABASE_URL: str = "sqlite:///./storage/app.db"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"
    FRONTEND_HOST: str

    APP_NAME: str = "VoteApp"
    APP_VERSION: str
    APP_DESCRIPTION: str = "Simple app to vote"


config = Config()
