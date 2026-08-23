"""
Eclipse API configuration.

Production fails closed if SECRET_KEY is missing or still the development placeholder.
"""

from __future__ import annotations

import sys
from typing import List, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


DEV_SECRET_PLACEHOLDER = "change-me-in-production-use-hsm"


class Settings(BaseSettings):
    PROJECT_NAME: str = "Project Eclipse"
    VERSION: str = "2.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = Field(default="development", description="development | staging | production")

    SECRET_KEY: str = Field(default=DEV_SECRET_PLACEHOLDER)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"

    CORS_ORIGINS: List[str] = Field(
        default_factory=lambda: ["http://localhost:5173", "http://localhost:3000"]
    )
    CORS_ALLOW_CREDENTIALS: bool = True

    ENABLE_DOCS: bool = True

    DATABASE_URL: str = "postgresql+asyncpg://eclipse:eclipse_dev@localhost:5432/eclipse"
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "eclipse_dev"
    ELASTICSEARCH_URL: str = "http://localhost:9200"
    ELASTICSEARCH_USERNAME: Optional[str] = None
    ELASTICSEARCH_PASSWORD: Optional[str] = None
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_PASSWORD: Optional[str] = None

    KAFKA_BOOTSTRAP: str = "localhost:9092"
    KAFKA_TOPIC_TRANSACTIONS: str = "eclipse.transactions"
    KAFKA_TOPIC_ALERTS: str = "eclipse.alerts"
    KAFKA_TOPIC_ENTITIES: str = "eclipse.entities"
    KAFKA_SECURITY_PROTOCOL: str = "PLAINTEXT"

    RISK_HIGH: int = 75
    RISK_MEDIUM: int = 40

    RATE_LIMIT_LOGIN_PER_MINUTE: int = 10
    RATE_LIMIT_REGISTER_PER_MINUTE: int = 5
    RATE_LIMIT_DEFAULT_PER_MINUTE: int = 120

    class Config:
        env_file = ".env"
        case_sensitive = True

    @field_validator("SECRET_KEY")
    @classmethod
    def secret_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("SECRET_KEY must not be empty")
        return v

    def validate_production_secrets(self) -> None:
        if self.ENVIRONMENT.lower() != "production":
            return
        if self.SECRET_KEY == DEV_SECRET_PLACEHOLDER:
            raise RuntimeError(
                "FATAL: Production cannot start with development SECRET_KEY placeholder. "
                "Set SECRET_KEY via environment or secrets manager."
            )
        if len(self.SECRET_KEY) < 32:
            raise RuntimeError(
                "FATAL: Production SECRET_KEY must be at least 32 characters."
            )
        if "eclipse_dev" in self.DATABASE_URL or "eclipse:eclipse_dev" in self.DATABASE_URL:
            raise RuntimeError(
                "FATAL: Production cannot use development database credentials."
            )
        if self.NEO4J_PASSWORD in ("eclipse_dev", "neo4j", "password", ""):
            raise RuntimeError(
                "FATAL: Production Neo4j password must not be a development default."
            )
        if not self.CORS_ORIGINS or "*" in self.CORS_ORIGINS:
            raise RuntimeError(
                "FATAL: Production CORS_ORIGINS must be an explicit allow-list (no '*')."
            )


def load_settings() -> Settings:
    settings = Settings()
    try:
        settings.validate_production_secrets()
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1) from exc
    return settings


settings = load_settings()
