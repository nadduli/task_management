#!/usr/bin/python3
"""configuration file to read environment variables"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """class Settings"""

    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


Config = Settings()
