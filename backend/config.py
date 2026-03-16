"""Application configuration using Pydantic Settings."""

from functools import lru_cache
from typing import Literal

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Database
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/scholybud",
        description="Database connection URL for production"
    )
    test_database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/scholybud_test",
        description="Database connection URL for testing"
    )

    # JWT
    secret_key: str = Field(
        default="change-this-secret-key-in-production",
        description="Secret key for JWT token encoding"
    )
    algorithm: str = Field(
        default="HS256",
        description="JWT algorithm"
    )
    access_token_expire_minutes: int = Field(
        default=10080,
        description="JWT access token expiration time in minutes (7 days)"
    )

    # CORS
    frontend_url: str = Field(
        default="http://localhost:5173",
        description="Frontend URL for CORS"
    )

    # Environment
    environment: Literal["development", "testing", "production"] = Field(
        default="development",
        description="Application environment"
    )

    @model_validator(mode="after")
    def validate_production_settings(self) -> "Settings":
        """Validate that production environment has secure settings."""
        if self.environment == "production":
            if self.secret_key == "change-this-secret-key-in-production" or self.secret_key == "dev-secret-key-change-in-production":
                raise ValueError(
                    "SECRET_KEY must be set in production. "
                    "Generate a secure key with: python -c 'import secrets; print(secrets.token_urlsafe(32))'"
                )
            if "postgres:postgres" in self.database_url:
                raise ValueError(
                    "Default database credentials detected. "
                    "Set DATABASE_URL with secure credentials in production."
                )
        return self


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
