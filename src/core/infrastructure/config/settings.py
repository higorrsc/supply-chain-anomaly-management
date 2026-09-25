from typing import Literal
from urllib.parse import quote_plus

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Load and validate environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # =========================
    # TEST
    # =========================

    test_in_memory: bool = True

    # =========================
    # DB ENV VARS
    # =========================

    db_host: str = Field(default="localhost")
    db_port: int = Field(default=5432)
    db_name: str | None = Field(default=None)
    db_user: str | None = Field(default=None)
    db_password: str | None = Field(default=None)

    @model_validator(mode="after")
    def validate_database_settings(self) -> Settings:
        """Validate database settings according to the execution mode."""

        if self.test_in_memory:
            return self

        missing = [
            name
            for name, value in {
                "DB_NAME": self.db_name,
                "DB_USER": self.db_user,
                "DB_PASSWORD": self.db_password,
            }.items()
            if not value
        ]

        if missing:
            raise ValueError(
                f"Missing required database settings: {', '.join(missing)}"
            )

        return self

    @property
    def database_url(self) -> str:
        """Build the asynchronous PostgreSQL connection URL."""

        if self.test_in_memory:
            return "sqlite+aiosqlite:///:memory:"

        if not all(
            (
                self.db_name,
                self.db_user,
                self.db_password,
            )
        ):
            raise RuntimeError("Database settings are incomplete.")

        user = quote_plus(self.db_user)  # type: ignore
        password = quote_plus(self.db_password)  # type: ignore

        return (
            f"postgresql+asyncpg://"
            f"{user}:{password}"
            f"@{self.db_host}:{self.db_port}"
            f"/{self.db_name}"
        )

    # =========================
    # AUTH
    # =========================

    secret_key: str = "change-me"
    algorithm: str = "HS256"

    # =========================
    # LOGGING
    # =========================

    log_level: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "INFO"


settings = Settings()
