from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = "Project Eclipse"
    VERSION: str = "2.0.0"
    API_V1_STR: str = "/api/v1"

    # Security
    SECRET_KEY: str = "change-me-in-production-use-hsm"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    # Databases
    DATABASE_URL: str = "postgresql+asyncpg://eclipse:eclipse_dev@localhost:5432/eclipse"
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "eclipse_dev"
    ELASTICSEARCH_URL: str = "http://localhost:9200"
    REDIS_URL: str = "redis://localhost:6379"

    # Kafka
    KAFKA_BOOTSTRAP: str = "localhost:9092"
    KAFKA_TOPIC_TRANSACTIONS: str = "eclipse.transactions"
    KAFKA_TOPIC_ALERTS: str = "eclipse.alerts"
    KAFKA_TOPIC_ENTITIES: str = "eclipse.entities"

    # Risk scoring thresholds
    RISK_HIGH: int = 75
    RISK_MEDIUM: int = 40

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
