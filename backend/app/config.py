from pathlib import Path
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class AuthSettings(BaseSettings):
    jwt_secret_key: SecretStr = Field(min_length=64)
    access_token_expire_minutes: int = Field(default=30, ge=1)

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        hide_input_in_errors=True,
    )

auth_settings = AuthSettings()