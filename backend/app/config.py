from functools import lru_cache
from pathlib import Path
from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict

_ENV_FILE = Path(__file__).resolve().parent.parent / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = ""
    db_name: str = "education_portal"
    secret_key: str = "dev-only-change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 480
    azure_ai_endpoint: str = ""
    azure_ai_key: str = ""
    azure_ai_api_key: str = ""
    azure_ai_model: str = "model-router"
    azure_ai_api_version: str = "v1"
    azure_ai_timeout_seconds: float = 20

    @property
    def azure_key(self) -> str:
        return self.azure_ai_key or self.azure_ai_api_key

    def _auth(self) -> str:
        user = quote_plus(self.db_user)
        if self.db_password:
            return f"{user}:{quote_plus(self.db_password)}"
        return user

    @property
    def database_url(self) -> str:
        return (
            f"mysql+pymysql://{self._auth()}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def server_database_url(self) -> str:
        """Connect without a schema so we can CREATE DATABASE IF NOT EXISTS."""
        return f"mysql+pymysql://{self._auth()}@{self.db_host}:{self.db_port}/"


@lru_cache
def get_settings() -> Settings:
    return Settings()
